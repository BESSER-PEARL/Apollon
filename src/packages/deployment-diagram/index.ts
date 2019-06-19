import { UMLElement } from '../../typings';

export enum DeploymentElementType {
  DeploymentNode = 'DeploymentNode',
  DeploymentArtifact = 'DeploymentArtifact',
}

export enum DeploymentRelationshipType {
  DeploymentAssociation = 'DeploymentAssociation',
}

export interface UMLDeploymentNode extends UMLElement {
  stereotype: string;
}