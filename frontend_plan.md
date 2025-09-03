# Frontend Implementation Plan: Onboarding-as-a-Service (OaaS)

## Technology Stack
- **Framework:** Next.js (latest version)
- **State Management:** React Context, Redux, or similar
- **Styling:** Tailwind CSS, CSS-in-JS, or similar
- **API Communication:** REST (fetch/axios), SWR/React Query
- **Authentication:** JWT/session-based, integrated with backend

---

## Milestone 1: Project Setup & Core Layout
- Initialize Next.js project with TypeScript
- Set up global styling and theming support
- Configure routing structure for multi-tenant (custom URL/subdomain) support
- Implement base layout (header, sidebar, main content)

---

## Milestone 2: Company Admin Web Portal
### 2.1 Authentication & Tenant Management
- Login/Logout pages for company admins
- Registration/invite flow for new company admins
- Tenant context switching (if multi-tenant admin)

### 2.2 Onboarding Flow Builder
- Dashboard for listing existing onboarding flows
- Create/Edit onboarding flow (drag-and-drop builder for stages)
- Stage configuration UI (text, media, forms, links)
- Theming & branding settings (logo, colors, etc.)

### 2.3 New Hire Management
- Assign new hires to onboarding flows
- List/search/filter new hires
- View new hire progress
- Trigger/send onboarding invitations

<!-- To be implemented in future version -->
### 2.4 Analytics & Reporting
- Dashboard with onboarding completion stats
- Custom report generation UI
- Export/download reports

<!-- To be implemented in future version -->
### 2.5 Integration Settings
- UI for configuring integrations (HRIS, ATS, e-signature, etc.)
- Webhook/API key management

### 2.6 Notification Templates
- Manage email/SMS/in-app notification templates
- Preview and test notifications

---

## Milestone 3: New Hire Onboarding Portal
### 3.1 Onboarding Entry & Session Management
- Landing page for onboarding via custom Subdomain (e.g., companyName.onboarding.com)
- Session token handling (from URL or cookie)
- Resume onboarding without login (using session token)

### 3.2 Dynamic Flow Rendering
- Fetch and render assigned onboarding flow and stages
- Support for text, media, forms, links, embedded content
- Progress tracking UI (steps, completion bar)
- Save progress as user advances

### 3.3 Feedback & Support
- Feedback form for new hires
- Help/FAQ section
- Contact support option

---

## Milestone 4: Shared Components & Utilities
### 4.1 Component Architecture Strategy
**Separation of Concerns:**
- **Admin Portal Components:** Focus on data configuration and content setup
- **New Hire Portal Components:** Focus on data collection and user interaction
- **Shared Components:** Only truly reusable UI elements (buttons, modals, etc.)

### 4.2 Admin Portal Components (Data Configuration)
- Content block configuration forms
- Validation rule editors
- Display settings panels
- Template selection and customization UI
- Drag-and-drop stage builder
- Content type selector with preview

### 4.3 New Hire Portal Components (Data Collection)
- Form input components with validation
- Progress indicators and navigation
- File upload interfaces
- Interactive content viewers
- Submission and save functionality

### 4.4 Shared Components
- Reusable form components (inputs, selects, file uploads)
- Media upload/viewer components
- Notification/toast system
- Error and loading states
- API client abstraction
- Common UI elements (buttons, modals, cards)

### 4.5 Component Benefits
- **Maintainability:** Clear separation prevents complex conditional logic
- **Performance:** Components optimized for their specific use case
- **Testing:** Easier to test focused components
- **Development:** Teams can work on different components independently
- **Scalability:** New features can be added without affecting existing components

---

## Milestone 5: Theming, Branding, and Accessibility
- Company-specific theming (colors, logos, etc.)
- Responsive design for all devices
- Accessibility (WCAG) compliance

---

## Milestone 6: QA, Testing, and Deployment
- Unit and integration tests (Jest, React Testing Library)
- End-to-end tests (Cypress/Playwright)
- CI/CD pipeline setup (GitHub Actions, Vercel, etc.)
- Production deployment and monitoring

---

## Notes
- All API endpoints and data models will be finalized after wireframes and backend planning.
- The plan assumes a clear separation between admin and new hire portals, but both are implemented in the same Next.js codebase for maintainability.
- Multi-tenancy and custom subdomain support are core to routing and theming from the start.
- **Component Strategy:** Admin and new hire portals use different component sets to maintain separation of concerns and prevent components from becoming overly complex with conditional logic.