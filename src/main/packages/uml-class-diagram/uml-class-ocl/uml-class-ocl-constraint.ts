import { DeepPartial } from 'redux';
import { UMLElementType } from '../../uml-element-type';
import { ILayer } from '../../../services/layouter/layer';
import { ILayoutable } from '../../../services/layouter/layoutable';
import { IUMLElement, UMLElement } from '../../../services/uml-element/uml-element';

export interface IUMLClassOCLConstraint extends IUMLElement {
  constraint: string;
}

export class ClassOCLConstraint extends UMLElement implements IUMLClassOCLConstraint {
  type: UMLElementType = UMLElementType.ClassOCLConstraint;
  constraint: string = '';

  constructor(values?: DeepPartial<IUMLClassOCLConstraint>) {
    super(values);
    if (values?.constraint !== undefined) {
      this.constraint = values.constraint;
    }
    this.adjustSizeToContent();
  }

  serialize() {
    return {
      ...super.serialize(),
      constraint: this.constraint
    };
  }

  deserialize(values: any) {
    super.deserialize(values);
    this.constraint = values.constraint || '';
  }


  private wrapText(text: string, maxWidth: number): string[] {
    if (!text) return [];
    
    const words = text.split(' ');
    const lines: string[] = [];
    let currentLine = '';
    const charsPerLine = Math.floor((maxWidth - 40) / 8); // Account for padding

    for (const word of words) {
      if ((currentLine + ' ' + word).length <= charsPerLine) {
        currentLine = currentLine ? currentLine + ' ' + word : word;
      } else {
        if (currentLine) lines.push(currentLine);
        if (word.length > charsPerLine) {
          // Split long words
          const chunks = word.match(new RegExp(`.{1,${charsPerLine}}`, 'g')) || [];
          lines.push(...chunks.slice(0, -1));
          currentLine = chunks[chunks.length - 1] || '';
        } else {
          currentLine = word;
        }
      }
    }
    if (currentLine) lines.push(currentLine);
    return lines;
  }

  private adjustSizeToContent() {
    const minWidth = 160;
    const minHeight = 50;
    const maxWidth = Math.max(minWidth, this.bounds.width || 400);
    const maxHeight = Math.max(minHeight, this.bounds.height || 200);

    if (this.constraint) {
      const lines = this.wrapText(this.constraint, maxWidth);
      const textHeight = Math.min((lines.length * 20) + 20, maxHeight);
      this.bounds.height = textHeight;
    }
  }

  render(canvas: ILayer): ILayoutable[] {
    return [this];
  }
}