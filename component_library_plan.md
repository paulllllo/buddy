# Component Library Implementation Plan

This document outlines the plan for creating a reusable component library for the Onboarding-as-a-Service (OaaS) application. The library will be published to npm and used by the new hire portal to dynamically render content.

## I. Core Technologies & Principles

*   **Framework**: React with TypeScript
*   **Bundler**: Rollup.js
*   **Testing**: Jest & React Testing Library
*   **Component Visualization**: Storybook
*   **Linting**: ESLint
*   **Pre-commit Hooks**: Husky
*   **Commit Standardization**: Conventional Commits
*   **CI/CD**: CircleCI for automated testing and publishing to npm

## II. Project Setup and Scaffolding

1.  **Create Project Directory**:
    *   Create a new directory named `component-library` in the root of the project.

2.  **Initialize Node.js Project**:
    *   Run `npm init` to create a `package.json` file.

3.  **Install Core Dependencies**:
    *   `react`, `react-dom`, and `typescript`.
    *   `@types/react`, `@types/react-dom`.

4.  **Configure TypeScript**:
    *   Create a `tsconfig.json` file with appropriate settings for a React library, including JSX support and module output.

5.  **Set up Rollup.js**:
    *   Install Rollup and necessary plugins (`@rollup/plugin-typescript`, `@rollup/plugin-commonjs`, `@rollup/plugin-node-resolve`, `rollup-plugin-postcss`).
    *   Create a `rollup.config.js` file to handle TypeScript compilation, CSS bundling, and generating different module formats (ESM, CJS).

## III. Component Development

1.  **Component Structure**:
    *   Each component will reside in its own directory under `src/components`.
    *   Component directory will contain:
        *   `index.tsx`: The component code.
        *   `styles.css`: Component-specific styles.
        *   `stories.tsx`: Storybook stories for the component.
        *   `test.tsx`: Jest tests for the component.

2.  **Dynamic Component Design**:
    *   Components will accept a `config` prop to control their structure and appearance, and a `content` prop for the data, mirroring the `ContentBlock` model from the backend.
    *   Initial components to be developed will be based on the `ContentType` model:
        *   `Header`
        *   `Description`
        *   `TextInput`
        *   `Checklist`
        *   `Media` (Image/Video)

## IV. Tooling and Best Practices

1.  **Storybook Integration**:
    *   Install and configure Storybook for React.
    *   Create stories for each component to visualize different states and variations based on the `config` prop.

2.  **Jest and React Testing Library**:
    *   Install Jest, React Testing Library, and necessary Babel dependencies (`@babel/preset-env`, `@babel/preset-react`, `@babel/preset-typescript`).
    *   Configure Jest to work with TypeScript and CSS modules.
    *   Write unit and integration tests for each component, covering rendering, user interactions, and edge cases.

3.  **ESLint and Prettier**:
    *   Set up ESLint with plugins for React, TypeScript, and accessibility.
    *   Configure Prettier for consistent code formatting.
    *   Add an ESLint script to `package.json`.

4.  **Husky and Conventional Commits**:
    *   Install Husky and `commitlint`.
    *   Configure Husky to run linting and tests on pre-commit.
    *   Configure `commitlint` to enforce conventional commit messages.

## V. CI/CD and Publishing

1.  **CircleCI Configuration**:
    *   Create a `.circleci/config.yml` file.
    *   Define a workflow with the following jobs:
        *   `build`: Install dependencies and build the library.
        *   `test`: Run all tests.
        *   `publish`: Publish the package to npm on pushes to the `main` branch.

2.  **NPM Publishing**:
    *   Configure `package.json` with the library name, version, entry points (`main`, `module`, `types`), and repository URL.
    *   The `publish` job in CircleCI will use an npm authentication token (stored as a secret) to publish the package.
    *   Versioning will be managed manually or with a tool like `semantic-release` in a future iteration.

## VI. Plan Execution (Todo List)

This plan will be executed via a series of smaller, actionable steps tracked in a TODO list.
