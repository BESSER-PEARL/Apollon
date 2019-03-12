import Element from './../Element';
import Port from '../Port';

abstract class Relationship extends Element {
  readonly base: string = 'Relationship';
  kind = 'Relationship';

  sourceRole: string = '';
  sourceMultiplicity: string = '';
  targetRole: string = '';
  targetMultiplicity: string = '';

  path: { x: number; y: number }[] = [{ x: 0, y: 0 }, { x: 0, y: 0 }];

  constructor(name: string, public source: Port, public target: Port) {
    super(name);
  }
}

export default Relationship;
