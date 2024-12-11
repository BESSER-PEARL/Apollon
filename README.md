

# BESSER GUI: A UML Modeling Editor

BESSER GUI is a UML modeling editor customized for the [BESSER platform](https://github.com/BESSER-PEARL/BESSER). It integrates BESSER's B-UML modeling language with powerful code generation capabilities, making it easy to design and generate code for software applications in a low-code environment.

## About BESSER GUI

BESSER GUI enhances the UML modeling experience with added support for BESSER’s B-UML language. Designed for seamless integration with the BESSER low-code platform, the editor provides tools for creating, editing, and generating code from UML diagrams.

## Key Features

### B-UML Modeling
- **Support for Structural and StateMachine Models**: Tailored to B-UML
- **Code Generation**: Automatically translate models into executable code for various applications, such as:
  - Python code compatible with the BESSER framework
  - Django models
  - SQLAlchemy database schemas


### Core Features
- **Intuitive Editor**:
  - Drag-and-drop interface
  - Text editing via double-click
  - Dark/light themes
- **Advanced Canvas**:
  - Infinite grid-based canvas
  - Flexible element positioning
  - Automatic relationship routing with manual waypoint adjustments
- **Diagram Support**:
  - Class Diagram
  - State Machine Diagram

### Integration with BESSER Platform
- **Automatic Saving**: Syncs with the BESSER backend.
- **Collaborative Editing**: Built for team-based modeling.
- **Code Generators**: Direct pipeline to BESSER's model-driven code generators.

## Installation
### Development
#### Clone the Repository
```bash
git clone https://github.com/besser/besser-gui.git
cd besser-gui
```

#### Install Dependencies
```bash
npm install
```

#### Start the Development Server
```bash
npm run start
```
The editor will be accessible at http://localhost:8888.

### Documentation
To build and serve the documentation locally:
```bash
npm run docs:prepare
npm run docs:build
npm run docs:watch
```
Documentation is served at http://localhost:8088.

### Contributing
We welcome contributions! Please ensure that any updates maintain compatibility with the BESSER platform. For major changes, please open an issue to discuss them before submitting a pull request.

Refer to the CONTRIBUTING.md for more details.

### License
This project is licensed under the MIT License.

### About the BESSER Platform
BESSER (Building bEtter Smart Software fastER) is a low-code platform designed for rapid software development, using B-UML as its core modeling language. For more information, visit the official BESSER documentation or explore the BESSER GitHub repository.
