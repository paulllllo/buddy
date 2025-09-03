# Frontend Implementation Plan (v3): Onboarding-as-a-Service (OaaS)

This plan provides a detailed roadmap for implementing the OaaS frontend, taking into account the existing backend architecture, API endpoints, and data schemas. It has been updated to reflect a focus on the Admin Portal first, with specific technology choices.

## 1. Core Principles & Technology Stack

### Principles
- **API-First:** The frontend is a consumer of the backend's OpenAPI-documented endpoints.
- **Component-Driven:** Build a reusable and maintainable component library.
- **Separation of Concerns:** The **Admin Portal** and **New Hire Portal** are separate applications.
- **Automated Schema Generation:** Frontend types and API services will be generated from the backend's OpenAPI specification to ensure consistency.

### Technology Stack
- **Framework:** Next.js (with TypeScript)
- **API Communication:** Orval to generate a client with Axios hooks.
- **State Management:** Axios for server state, Zustand for global UI state.
- **UI Components:** shadcn/ui, built on Tailwind CSS.
- **Forms:** React Hook Form for building and validating forms.

---

## 2. Project Structure (Admin Portal)

We will start with a single application for the Admin Portal.

```
admin-portal/
├── app/                    # Next.js App Router
├── components/
│   ├── ui/                 # shadcn/ui components
│   └── shared/             # Custom shared components (e.g., PageHeader)
├── lib/
│   ├── api/                # Generated API client (by Orval)
│   └── utils.ts            # Utility functions
├── orval.config.js         # Orval configuration file
└── package.json
```

---

## 3. API Client & Schema Generation

A critical first step is to set up a process for generating the frontend API client from the backend's OpenAPI specification.

- **Tooling:** Use **Orval** with the React Query processor.
- **Workflow:**
    1.  The backend serves its OpenAPI schema at `/openapi.json`.
    2.  An Orval script fetches this schema.
    3.  Orval generates TypeScript types for all API schemas (`UserCreate`, `FlowResponse`, etc.).
    4.  It also generates typed React Query hooks for each API endpoint (e.g., `useGetFlows()`, `useCreateNewHire()`).
- **Benefit:** This eliminates manual creation of frontend types and API service layers, reducing errors and ensuring the frontend is always in sync with the backend.

---

## 4. Milestone 1: Admin Portal - Core Setup & Authentication

- **[ ] Task 1.1: Project Initialization:** Initialize a new Next.js project for the `admin-portal`.
- **[ ] Task 1.2: UI & Styling Setup:** Integrate Tailwind CSS and set up `shadcn/ui`.
- **[ ] Task 1.3: API Client Generation:** Configure Orval to generate the API client from the backend's `/openapi.json`.
- **[ ] Task 1.4: Authentication:**
    - Implement Register (`/register`) and Login (`/login`) pages using the generated API hooks.
    - Use the `UserCreate` and `UserLogin` schemas for form validation with React Hook Form.
    - Implement JWT storage (secure, HTTP-only cookie) and token refresh logic.
    - Create a protected route HOC for the admin dashboard.

---

## 5. Milestone 2: Admin Portal - Dashboard & Flow Management

### 5.1 Dashboard & Company Management
- **[ ] Task 2.1: Main Dashboard Layout:** Create the main layout with a sidebar and header using `shadcn/ui` components.
- **[ ] Task 2.2: Company Settings Page:**
    - Fetch company data using the generated `useGetCompanyInfo` hook.
    - Create a form to update company info (`CompanyUpdate` schema).
    - Implement logo upload functionality.
    - Implement a branding section to update theme colors.

### 5.2 Onboarding Flow Management
- **[ ] Task 2.3: Flows List Page:**
    - Fetch and display all flows for the company using the `useListFlows` hook.
    - Implement "Create New Flow" functionality in a modal or separate page (`FlowCreate` schema).
- **[ ] Task 2.4: Flow Detail & Editor Page:**
    - Display flow details using the `useGetFlow` hook.
    - Allow updating flow details (`FlowUpdate` schema).
    - List stages for the flow using the `useListStages` hook.
    - Implement drag-and-drop reordering for stages.

### 5.3 Stage & Content Block Editor
- **[ ] Task 2.5: Stage Editor:**
    - Allow creating new stages (`StageCreate` schema).
    - Allow updating stage details (`StageUpdate` schema).
- **[ ] Task 2.6: Content Block Editor:**
    - Fetch and display all content blocks for a stage.
    - Implement an "Add Content Block" feature, allowing the user to select from available `content_types`.
    - Create a dynamic form for creating/editing content blocks based on the selected `type` and its corresponding schema.
    - Implement drag-and-drop reordering for content blocks.

### 5.4 New Hire Management
- **[ ] Task 2.7: New Hires List Page:**
    - Fetch and display all new hires.
    - Implement functionality to invite a new hire (`NewHireCreate` schema).
- **[ ] Task 2.8: New Hire Detail Page:**
    - Display new hire details and their progress.

---

## 6. Milestone 3: Deployment & Finalization

- **[ ] Task 3.1: CI/CD Pipeline:** Set up GitHub Actions to build, test, and deploy the Admin Portal application (e.g., to Vercel).
- **[ ] Task 3.2: Testing:** Write unit and integration tests for critical components and API hooks.
- **[ ] Task 3.3: End-to-End Testing:** Use Cypress or Playwright to test key user flows (admin login, creating a flow, inviting a user).

---

## Future Milestones: New Hire Onboarding Portal

The New Hire Portal will be developed as a separate project after the Admin Portal is complete. It will have its own distinct architecture, potentially using more custom components to accommodate dynamic branding and content rendering. It will also leverage an Orval-generated API client with relevant endpoints for consistency.