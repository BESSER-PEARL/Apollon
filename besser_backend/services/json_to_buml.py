import uuid
from besser.BUML.metamodel.structural import DomainModel, Class, Enumeration, Property, Method, BinaryAssociation, \
    Generalization, PrimitiveDataType, EnumerationLiteral, Multiplicity, UNLIMITED_MAX_MULTIPLICITY
from utils.constants import VISIBILITY_MAP, VALID_PRIMITIVE_TYPES
from utils.constants import VISIBILITY_MAP, RELATIONSHIP_TYPES
from .layout_calculator import (
    determine_connection_direction, calculate_connection_points,
    calculate_path_points, calculate_relationship_bounds
)

def parse_attribute(attribute_name, domain_model=None):
    """Parse an attribute string to extract visibility, name, and type, removing any colons."""
    parts = attribute_name.replace(":", "").split()  # Remove colons from the attribute name
    if len(parts) == 1:
        visibility = "public"
        name = parts[0]
        attr_type = "str"
    else:
        visibility_symbol = parts[0] if parts[0] in VISIBILITY_MAP else "+"
        visibility = VISIBILITY_MAP.get(visibility_symbol, "public")  # Default to "public"
        name = parts[1] if len(parts) > 1 else "Unnamed"
        
        # Check if type is specified
        if len(parts) > 2:
            type_name = parts[2]
            # Check if type is an enumeration in the domain model
            if domain_model and any(isinstance(t, Enumeration) and t.name == type_name for t in domain_model.types):
                attr_type = type_name  # Keep the enumeration type name
            else:
                # Convert to primitive type if not an enumeration
                attr_type = VALID_PRIMITIVE_TYPES.get(type_name.lower(), "str")
        else:
            attr_type = "str"  # Default to "str" if no type specified
            
    return visibility, name, attr_type

def parse_method(method_str):
    """
    Parse a method string to extract visibility, name, parameters, and return type.
    Examples:
    "+ notify(sms: str = 'message')" -> ("public", "notify", [{"name": "sms", "type": "str", "default": "message"}], None)
    "- findBook(title: str): Book" -> ("private", "findBook", [{"name": "title", "type": "str"}], "Book")
    "validate()" -> ("public", "validate", [], None)
    """
    import re

    # Default values
    visibility = "public"
    parameters = []
    return_type = None

    # Check if this is actually a method (contains parentheses)
    if '(' not in method_str:
        return visibility, method_str, parameters, return_type

    # Extract visibility if present
    if method_str.startswith(tuple(VISIBILITY_MAP.keys())):
        visibility = VISIBILITY_MAP.get(method_str[0], "public")
        method_str = method_str[2:].strip()

    # Parse method using regex
    pattern = r"([^(]+)\((.*?)\)(?:\s*:\s*(.+))?"
    match = re.match(pattern, method_str)
    
    if not match:
        return visibility, method_str.replace("()", ""), parameters, return_type

    method_name, params_str, return_type = match.groups()
    method_name = method_name.strip()

    # Parse parameters if present
    if params_str:
        # Handle nested parentheses in default values
        param_list = []
        current_param = []
        paren_count = 0
        
        for char in params_str + ',':
            if char == '(' and paren_count >= 0:
                paren_count += 1
                current_param.append(char)
            elif char == ')' and paren_count > 0:
                paren_count -= 1
                current_param.append(char)
            elif char == ',' and paren_count == 0:
                param_list.append(''.join(current_param).strip())
                current_param = []
            else:
                current_param.append(char)

        for param in param_list:
            if not param:
                continue
                
            param_dict = {'name': param, 'type': 'str'}  # Default type

            # Handle parameter with default value
            if '=' in param:
                param_parts = param.split('=', 1)
                param_name_type = param_parts[0].strip()
                default_value = param_parts[1].strip().strip('"\'')
                
                if ':' in param_name_type:
                    param_name, param_type = [p.strip() for p in param_name_type.split(':')]
                    param_dict.update({
                        'name': param_name,
                        'type': VALID_PRIMITIVE_TYPES.get(param_type.lower(), param_type),
                        'default': default_value
                    })
                else:
                    param_dict.update({
                        'name': param_name_type,
                        'default': default_value
                    })

            # Handle parameter with type annotation
            elif ':' in param:
                param_name, param_type = [p.strip() for p in param.split(':')]
                param_dict.update({
                    'name': param_name,
                    'type': VALID_PRIMITIVE_TYPES.get(param_type.lower(), param_type)
                })
            else:
                param_dict['name'] = param.strip()

            parameters.append(param_dict)

    # Clean up return type if present
    if return_type:
        return_type = return_type.strip()
        # Keep the original return type if it's not a primitive type
        # (it might be a class name)
        if return_type.lower() in VALID_PRIMITIVE_TYPES:
            return_type = VALID_PRIMITIVE_TYPES[return_type.lower()]

    return visibility, method_name, parameters, return_type

def parse_multiplicity(multiplicity_str):
    """Parse a multiplicity string and return a Multiplicity object with defaults."""
    if not multiplicity_str:
        return Multiplicity(min_multiplicity=1, max_multiplicity=1)
    
    parts = multiplicity_str.split("..")
    min_multiplicity = int(parts[0]) if parts[0] else 1
    max_multiplicity = (
        int(parts[1]) if len(parts) > 1 and parts[1] and parts[1] != "*" else UNLIMITED_MAX_MULTIPLICITY
    )
    return Multiplicity(min_multiplicity=min_multiplicity, max_multiplicity=max_multiplicity)

def json_to_buml(json_data):
    """Convert JSON data to a BUML DomainModel object."""
    domain_model = DomainModel("Domain Model")
    elements = json_data.get("elements", {}).get("elements", {})
    relationships = json_data.get("elements", {}).get("relationships", {})

    # First process enumerations to have them available for attribute types
    for element_id, element in elements.items():
        if element.get("type") == "Enumeration":
            element_name = element.get("name")
            literals = set()
            for literal_id in element.get("attributes", []):
                literal = elements.get(literal_id)
                if literal:
                    literal_obj = EnumerationLiteral(name=literal.get("name", ""))
                    literals.add(literal_obj)
            enum = Enumeration(name=element_name, literals=literals)
            domain_model.types.add(enum)

    # Then process classes with attributes that might reference enumerations
    for element_id, element in elements.items():
        # Check for both regular Class and AbstractClass
        if element.get("type") in ["Class", "AbstractClass"]:
            # Set is_abstract based on the type
            is_abstract = element.get("type") == "AbstractClass"
            cls = Class(name=element.get("name"), is_abstract=is_abstract)
            # Add attributes
            for attr_id in element.get("attributes", []):
                attr = elements.get(attr_id)
                if attr:
                    visibility, name, attr_type = parse_attribute(attr.get("name", ""), domain_model)
                    # If attr_type is a string matching an enumeration name, get the actual enumeration
                    if any(isinstance(t, Enumeration) and t.name == attr_type for t in domain_model.types):
                        enum_type = next(t for t in domain_model.types if isinstance(t, Enumeration) and t.name == attr_type)
                        property = Property(name=name, type=enum_type, visibility=visibility)
                    else:
                        property = Property(name=name, type=PrimitiveDataType(attr_type), visibility=visibility)
                    cls.attributes.add(property)

            # Add methods
            for method_id in element.get("methods", []):
                method = elements.get(method_id)
                if method:
                    visibility, name, parameters, return_type = parse_method(method.get("name", ""))
                    
                    # Create method parameters
                    method_params = []
                    for param in parameters:
                        param_type = PrimitiveDataType(param['type'])
                        param_obj = Property(
                            name=param['name'],
                            type=param_type,
                            visibility='public'
                        )
                        if 'default' in param:
                            param_obj.default_value = param['default']
                        method_params.append(param_obj)
                    
                    # Create method with parameters and return type
                    method_obj = Method(
                        name=name,
                        visibility=visibility,
                        parameters=method_params
                    )
                    # Handle return type
                    if return_type:
                        # Check if return type is a class in the domain model
                        return_class = domain_model.get_class_by_name(return_type)
                        if return_class:
                            method_obj.type = return_class
                        else:
                            # If not a class, treat as primitive type
                            method_obj.type = PrimitiveDataType(return_type)
                    cls.methods.add(method_obj)

            domain_model.types.add(cls)

    # Processing relationships (Associations, Generalizations, and Compositions)
    for rel_id, relationship in relationships.items():
        print(f"Processing relationship ID: {rel_id} with data: {relationship}")

        rel_type = relationship.get("type")
        source = relationship.get("source")
        target = relationship.get("target")

        if not rel_type or not source or not target:
            print(f"Skipping relationship {rel_id} due to missing data.")
            continue

        # Retrieve source and target elements
        source_element = elements.get(source.get("element"))
        target_element = elements.get(target.get("element"))

        if not source_element or not target_element:
            print(f"Skipping relationship {rel_id} due to missing elements.")
            continue

        source_class = domain_model.get_class_by_name(source_element.get("name", ""))
        target_class = domain_model.get_class_by_name(target_element.get("name", ""))

        if not source_class or not target_class:
            print(f"Skipping relationship {rel_id} because classes are missing in the domain model.")
            continue

        # Handle each type of relationship
        if rel_type == "ClassBidirectional" or rel_type == "ClassUnidirectional" or rel_type == "ClassComposition":
            is_composite = rel_type == "ClassComposition"
            source_navigable = rel_type != "ClassUnidirectional"
            target_navigable = True

            source_multiplicity = parse_multiplicity(source.get("multiplicity", "1"))
            target_multiplicity = parse_multiplicity(target.get("multiplicity", "1"))

            source_property = Property(
                name=source.get("role", ""),
                type=target_class,
                multiplicity=source_multiplicity,
                is_navigable=source_navigable,
                is_composite=is_composite
            )
            target_property = Property(
                name=target.get("role", ""),
                type=source_class,
                multiplicity=target_multiplicity,
                is_navigable=target_navigable
            )

            association = BinaryAssociation(
                name=f"{source_class.name}_{target_class.name}",
                ends={source_property, target_property}
            )
            domain_model.associations.add(association)

        elif rel_type == "ClassInheritance":
            generalization = Generalization(general=source_class, specific=target_class)
            domain_model.generalizations.add(generalization)

    return domain_model
