export const ClassElementType = {
  Package: 'Package',
  Class: 'Class',
  AbstractClass: 'AbstractClass',
  Interface: 'Interface',
  Enumeration: 'Enumeration',
  ClassAttribute: 'ClassAttribute',
  ClassMethod: 'ClassMethod',
  AbstractClass2: 'AbstractClass2',
} as const;

export const ClassRelationshipType = {
  ClassBidirectional: 'ClassBidirectional',
  ClassUnidirectional: 'ClassUnidirectional',
  ClassInheritance: 'ClassInheritance',
  ClassRealization: 'ClassRealization',
  ClassDependency: 'ClassDependency',
  ClassAggregation: 'ClassAggregation',
  ClassComposition: 'ClassComposition',
} as const;
