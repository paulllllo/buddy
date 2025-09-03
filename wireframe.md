<!-- Company Admin Dashboard -->

### **Page Information**
- **Page Name:** Company Admin Dashboard
- **URL Path:** "/dashboard"
- **User Type:** Admin
- **Purpose:** Overview of company's onboarding activities and quick access to key features and onboarding flows

### **Layout Structure**
```
Header: Company logo (left), user avatar with dropdown menu (right)
Sidebar: Navigation menu with icons and labels
  - Dashboard (active)
  - Onboarding Flows
  - New Hires
  - Settings
Breadcrumbs nav: to show user where they are in the app(based on routing)
Main Content: Grid of dashboard cards and recent activity list
  - Cards show a quick summary of app states(number of onboardings, few onboarding flows etc.)
Button to create new onboarding flow
Footer: None
```

### **Key UI Components**
- **Cards:** 4 or more dashboard cards showing stats (Active Flows, New Hires This Month, Completion Rate, Recent Activity)
- **Table:** Recent new hires with columns (Name, Assigned Flow, Progress %, Last Activity)
- **Button:** "Create New Flow" CTA button
- **Search:** Search bar for filtering new hires

### **Data Displayed**
- **Static Content:** Page title "Dashboard", card titles
- **Dynamic Data:** 
  - Dashboard stats (counts, percentages)
  - Recent new hires list

### **User Actions & Interactions**
- **Action:** Click "Create New Flow" button
- **Trigger:** CTA button in main content area
- **Frontend Request:** Navigate to "/flows/create"
- **Expected Response:** Load flow creation page
- **UI Update:** Page navigation
- **Error Handling:** None (simple navigation)

- **Action:** Click on new hire row
- **Trigger:** Table row click
- **Frontend Request:** Navigate to /new-hires/{id}
- **Expected Response:** New hire details
- **UI Update:** Navigate to new hire detail page
- **Error Handling:** Show error toast if API fails

### **API Endpoints Used**
- **GET /api/companies/{id}/dashboard-stats** - Fetch dashboard statistics
- **GET /api/companies/{id}/new-hires?limit=10** - Fetch recent new hires
- **GET /api/companies/{id}/flows?status=active** - Fetch active flows count

### **Database Entities Involved**
- **Primary Entities:** Company, OnboardingFlow, NewHire
- **Related Entities:** User (for admin info), Progress (for completion stats)
- **User Permissions:** Company admin access

### **State Management**
- **Local State:** Search filter text, selected tab
- **Global State:** Current company context, user info
- **Server State:** Dashboard stats, recent new hires list

### **Responsive Considerations**
- **Mobile:** Cards stack vertically, sidebar becomes hamburger menu
- **Tablet:** Cards in 2x2 grid, sidebar remains visible
- **Desktop:** Cards in single row, full sidebar visible

### **Accessibility Requirements**
- **Component Library** Use component libraries like radixUI or shadCN which have accessibility considerations
- **Keyboard Navigation:** All interactive elements keyboard accessible
- **Screen Readers:** Proper heading hierarchy, alt text for stats
- **Color Contrast:** High contrast for all text and interactive elements




### **Page Information**
- **Page Name:** Onboarding Flows List
- **URL Path:** "/flows"
- **User Type:** Admin
- **Purpose:** View, create, update, and navigate to onboarding flows for the company

### **Layout Structure**
```
Header: Company logo (left), user avatar with dropdown menu (right)
Sidebar: Navigation menu with icons and labels
  - Dashboard
  - Onboarding Flows (active)
  - New Hires
  - Settings
Breadcrumbs nav: to show user where they are in the app (e.g., Home / Onboarding Flows)
Main Content: 
  - Title: "Onboarding Flows"
  - Button: "Create New Onboarding Flow" (top right)
  - List of cards: All onboarding flows with data (Name, Description, Status, Created Date, Last Updated, Actions)
  - Each item has an action menu (Edit, Delete, View)
  - Clicking an item or 'View' navigates to the onboarding flow detail page
Footer: None
```

### **Key UI Components**
- **Items:** List of onboarding flows
- **Button:** "Create New Onboarding Flow" CTA
- **Action Menu:** Edit, Delete, View for each flow
- **Search/Filter:** Search bar and/or filters for flow name, status
- **Pagination:** If many flows

### **Data Displayed**
- **Static Content:** Page title, description
- **Dynamic Data:**
  - List of onboarding flows (Name, Description, Status, Created Date, Last Updated)
- **User Input:** Search/filter text, action menu selections

### **User Actions & Interactions**
- **Action:** Click "Create New Onboarding Flow" button
  - **Trigger:** CTA button
  - **Frontend Request:** Navigate to "/flows/create"
  - **Expected Response:** Load create onboarding flow page
  - **UI Update:** Page navigation
  - **Error Handling:** None (simple navigation)

- **Action:** Click on onboarding flow item or 'View' action
  - **Trigger:** Item or action menu
  - **Frontend Request:** Navigate to "/flows/{id}"
  - **Expected Response:** Load onboarding flow detail page
  - **UI Update:** Page navigation
  - **Error Handling:** Show error toast if API fails

- **Action:** Click 'Edit' in action menu
  - **Trigger:** Action menu
  - **Frontend Request:** Navigate to "/flows/{id}/edit"
  - **Expected Response:** Load edit onboarding flow page
  - **UI Update:** Page navigation
  - **Error Handling:** Show error toast if API fails

- **Action:** Click 'Delete' in action menu
  - **Trigger:** Action menu
  - **Frontend Request:** DELETE /api/flows/{id}
  - **Expected Response:** Remove flow from list
  - **UI Update:** Table updates, success/error toast
  - **Error Handling:** Show error toast if API fails

### **API Endpoints Used**
- **GET /api/companies/{id}/flows** - Fetch all onboarding flows
- **DELETE /api/flows/{id}** - Delete onboarding flow

### **Database Entities Involved**
- **Primary Entities:** OnboardingFlow, Company
- **Related Entities:** User (for created/updated by info), Flow(to get a flow details under a )
- **User Permissions:** Company admin access

### **State Management**
- **Local State:** Search/filter text, selected item, action menu state(likely handled by component library)
- **Global State:** Current company context, user info
- **Server State:** List of onboarding flows

### **Responsive Considerations**
- **Mobile:** Cards stack vertically, action menu as dropdown
- **Tablet:** Cards in 2x2 grid
- **Desktop:** Cards in 4x4 grid

### **Accessibility Requirements**
- **Component Library:** Use accessible table/list components
- **Keyboard Navigation:** All interactive elements keyboard accessible
- **Screen Readers:** Proper semantics, ARIA labels for actions
- **Color Contrast:** High contrast for all text and interactive elements




### **Page Information**
- **Page Name:** Create Onboarding Flow
- **URL Path:** "/flows/create"
- **User Type:** Admin
- **Purpose:** Create a new onboarding flow with metadata, branding, and support information

### **Layout Structure**
```
Header: Company logo (left), user avatar with dropdown menu (right)
Sidebar: Navigation menu with icons and labels
  - Dashboard
  - Onboarding Flows (active)
  - New Hires
  - Settings
Breadcrumbs nav: Home / Onboarding Flows / Create
Main Content:
  - Title: "Create New Onboarding Flow"
  - Form with sections:
    - Basic Info: Name, Description
    - Duration: Number input (days/weeks), optional start/end dates
    - Branding: Color pickers (Primary, Secondary, Accent), Logo upload
    - Support Info: Optional fields for support email, phone, help link
    - Other Metadata: Tags, status (draft/published), etc.
  - Button: "Create Onboarding Flow" (submits form and takes you to the specific onboarding details page)
Footer: None
```

### **Key UI Components**
- **Form:**
  - Name (required, text input)
  - Description (optional, textarea)
  - Duration (required, number input, select unit)
  - Branding:
    - Primary Color (color picker)
    - Secondary Color (color picker)
    - Accent Color (color picker)
    - Logo (file upload, image preview)
  - Support Info (optional):
    - Support Email (email input)
    - Support Phone (tel input)
    - Help Link (URL input)
  - Other Metadata:
    - Tags (multi-select or text input)
    - Status (dropdown: draft/published)
  - Submit Button: "Create Onboarding Flow"

### **Data Displayed**
- **Static Content:** Form labels, section headers, help text
- **Dynamic Data:** Logo preview, validation errors
- **User Input:** All form fields above

### **User Actions & Interactions**
- **Action:** Fill out form fields
  - **Trigger:** User types/selects/uploads
  - **Frontend Request:** Local state update
  - **Expected Response:** Form validation feedback
  - **UI Update:** Show errors, previews
  - **Error Handling:** Inline validation errors

- **Action:** Click "Create Onboarding Flow" button
  - **Trigger:** Submit button
  - **Frontend Request:** POST /api/companies/{id}/flows with form data
  - **Expected Response:** New onboarding flow created, returns new flow ID
  - **UI Update:** Navigate to "/flows/{id}" (details page)
  - **Error Handling:** Show error toast if API fails

### **API Endpoints Used**
- **POST /api/companies/{id}/flows** - Create new onboarding flow

### **Database Entities Involved**
- **Primary Entities:** OnboardingFlow, Company
- **Related Entities:** User (created by)
- **User Permissions:** Company admin access

### **State Management**
- **Local State:** Form field values, validation errors, logo preview
- **Global State:** Current company context, user info
- **Server State:** None until form submit

### **Responsive Considerations**
- **Mobile:** Form fields stack vertically, logo upload as full-width
- **Tablet:** Form in single column, larger inputs
- **Desktop:** Form sections in two columns if space allows

### **Accessibility Requirements**
- **Component Library:** Use accessible form components
- **Keyboard Navigation:** All form fields and buttons keyboard accessible
- **Screen Readers:** Proper labels, ARIA attributes for form fields
- **Color Contrast:** High contrast for all text and interactive elements




### **Page Information**
- **Page Name:** Onboarding Flow Details
- **URL Path:** "/flows/{id}"
- **User Type:** Admin
- **Purpose:** View and manage all details of a specific onboarding flow, including stages and user progress

### **Layout Structure**
```
Header: Company logo (left), user avatar with dropdown menu (right)
Sidebar: Navigation menu (Dashboard, Onboarding Flows, New Hires, Settings)
Breadcrumbs nav: Home / Onboarding Flows / [Flow Name]
Main Content:
  - Title: Flow Name
  - Basic Info: Description, Duration, Branding (colors, logo), Support Info, Status, etc.
  - Button: "Add Stage" (adds a new stage with default setup)
  - Tabs:
    1. Stages (default active):
      - Card grid view of all stages (Name, Type, Order, Status, etc.)
      - Each card clickable to open Stage Details page
    2. Pipeline:
      - Horizontal scrollable pipeline view
      - Each stage as a header/column
      - Under each stage, cards for users currently at that stage (Name, progress, etc.)
Footer: None
```

### **Key UI Components**
- **Tabs:** Stages, Pipeline
- **Card Grid:** Stages (with basic info, clickable)
- **Button:** "Add Stage"
- **Modal:** Stage creation form with metadata fields and template selection
- **Pipeline View:** Stages as columns, users as cards under current stage
- **Info Section:** Flow metadata (description, branding, etc.)

### **Data Displayed**
- **Static Content:** Section headers, tab labels
- **Dynamic Data:**
  - Flow metadata (name, description, duration, branding, support info, status)
  - List of stages (id, name, type, order, status)
  - List of users and their current stage (for pipeline)
  - Stage templates (for modal dropdown)

### **User Actions & Interactions**
- **Action:** Click "Add Stage" button
  - **Trigger:** Button
  - **Frontend Request:** None (local state)
  - **Expected Response:** Modal opens with stage creation form
  - **UI Update:** Modal appears with form
  - **Error Handling:** None (local state only)

- **Action:** Fill out stage metadata in modal
  - **Trigger:** User types/selects in form fields
  - **Frontend Request:** None (local state)
  - **Expected Response:** Form validation feedback
  - **UI Update:** Show validation errors, enable/disable create button
  - **Error Handling:** Inline validation errors

- **Action:** Select stage template from dropdown
  - **Trigger:** Dropdown selection
  - **Frontend Request:** None (local state)
  - **Expected Response:** Form fields populate with template data
  - **UI Update:** Form fields update with template values
  - **Error Handling:** None (local state only)

- **Action:** Click "Create Stage" button in modal
  - **Trigger:** Create button in modal
  - **Frontend Request:** POST /api/flows/{id}/stages (with form data and template)
  - **Expected Response:** New stage created successfully
  - **UI Update:** Modal closes, stage appears in grid and pipeline
  - **Error Handling:** Show error toast if API fails

- **Action:** Click "Cancel" button in modal
  - **Trigger:** Cancel button in modal
  - **Frontend Request:** None
  - **Expected Response:** Modal closes
  - **UI Update:** Modal disappears, form resets
  - **Error Handling:** None

- **Action:** Click on stage card
  - **Trigger:** Card click
  - **Frontend Request:** Navigate to "/flows/{id}/stages/{stageId}"
  - **Expected Response:** Load stage details page
  - **UI Update:** Page navigation
  - **Error Handling:** Show error toast if API fails

- **Action:** Switch tabs
  - **Trigger:** Tab click
  - **Frontend Request:** None (local state)
  - **Expected Response:** Show selected tab content
  - **UI Update:** Tab content changes
  - **Error Handling:** None

### **API Endpoints Used**
- **GET /api/flows/{id}** - Fetch flow details
- **GET /api/flows/{id}/stages** - Fetch all stages for flow
- **POST /api/flows/{id}/stages** - Add new stage
- **GET /api/flows/{id}/pipeline** - Fetch users and their current stage
- **GET /api/stage-templates** - Fetch available stage templates

### **Database Entities Involved**
- **Primary Entities:** OnboardingFlow, Stage
- **Related Entities:** User, Progress, New Hires, StageTemplate
- **User Permissions:** Company admin access

### **State Management**
- **Local State:** Active tab(probably managed by component library), selected stage, modal state, form data
- **Global State:** Current company context, user info
- **Server State:** Flow details, stages, NewHire data, stage templates

### **Responsive Considerations**
- **Mobile:** Tabs stack vertically, stage cards in single column, pipeline horizontally scrollable
- **Tablet:** Tabs and cards in 2-column grid, pipeline scrollable
- **Desktop:** Tabs and cards in multi-column grid, pipeline full width

### **Accessibility Requirements**
- **Component Library:** Use accessible tab, card, and pipeline components
- **Keyboard Navigation:** All interactive elements keyboard accessible
- **Screen Readers:** Proper ARIA roles for tabs, cards, pipeline
- **Color Contrast:** High contrast for all text and interactive elements




### **Page Information**
- **Page Name:** Stage Details
- **URL Path:** "/flows/{flowId}/stages/{stageId}"
- **User Type:** Admin
- **Purpose:** Configure the content and settings of a specific onboarding stage

### **Layout Structure**
```
Header: Company logo (left), user avatar with dropdown menu (right)
Sidebar: Navigation menu (Dashboard, Onboarding Flows, New Hires, Settings)
Breadcrumbs nav: Home / Onboarding Flows / [Flow Name] / [Stage Name]
Main Content:
  - Title: Stage Name
  - Section: List of content blocks (stacked vertically, each as a card/step)
    - Each content block shows type, summary, and has controls (move, delete, duplicate. content blocks are also draggable)
    - Add button between/after blocks to insert new content at any point
  - When a content block is clicked:
    - Highlighted visually
    - Config Bar appears on the right
      - Content Type selector (always visible on config bar while others are dynamic)
      - Config fields (dependent on content type)
Footer: None
```

### **Key UI Components**
- **Content Block List:** Stacked cards/steps for each content item(cards are draggable to any position)
- **Add Button:** Insert content at any position
- **Config Bar:** Appears on right when content is selected, shows config fields
- **Content Type Selector:** Dropdown/select (always visible in config bar)
- **Config Fields:** Dynamic, based on content type
- **Controls:** Move, delete, duplicate for each content block

### **Data Displayed**
- **Static Content:** Section headers, help text
- **Dynamic Data:** 
  - List of content blocks (type, summary, order, config)
  - Config bar fields (based on selected content type)
- **User Input:** Content block edits, config changes

### **User Actions & Interactions**
- **Action:** Click add button to insert content
  - **Trigger:** Add button
  - **Frontend Request:** POST /api/flows/{flowId}/stages/{stageId}/contents (with default data and position)
  - **Expected Response:** New content block added
  - **UI Update:** Content appears in list
  - **Error Handling:** Show error toast if API fails

- **Action:** Click content block
  - **Trigger:** Card click
  - **Frontend Request:** None (local state)
  - **Expected Response:** Config bar appears, block is highlighted
  - **UI Update:** Show config bar, highlight block
  - **Error Handling:** None

- **Action:** Change content type in config bar
  - **Trigger:** Dropdown/select in config bar
  - **Frontend Request:** None (local state update)
  - **Expected Response:** Config bar fields update to show new type's fields
  - **UI Update:** Show new config fields for selected type
  - **Error Handling:** None (local state only)

- **Action:** Edit config fields
  - **Trigger:** Input/change in config bar
  - **Frontend Request:** None (local state update)
  - **Expected Response:** Config fields update locally
  - **UI Update:** Config fields update
  - **Error Handling:** None (local state only)

- **Action:** Click "Save Stage" button
  - **Trigger:** Save button
  - **Frontend Request:** PATCH /api/flows/{flowId}/stages/{stageId} (all stage changes)
  - **Expected Response:** Stage updated successfully
  - **UI Update:** Success toast, any visual updates
  - **Error Handling:** Show error toast if API fails

- **Action:** Move, delete, duplicate content block
  - **Trigger:** Controls on block
  - **Frontend Request:** PATCH/DELETE/POST as appropriate
  - **Expected Response:** List updates
  - **UI Update:** Content order/appearance updates
  - **Error Handling:** Show error toast if API fails

### **API Endpoints Used**
- **GET /api/flows/{flowId}/stages/{stageId}** - Fetch stage details
- **GET /api/flows/{flowId}/stages/{stageId}/contents** - Fetch all content blocks
- **POST /api/flows/{flowId}/stages/{stageId}/contents** - Add new content block
- **PATCH /api/flows/{flowId}/stages/{stageId}** - Update stage (all content and config changes)
- **DELETE /api/flows/{flowId}/stages/{stageId}/contents/{contentId}** - Delete content block

### **Database Entities Involved**
- **Primary Entities:** Stage, ContentBlock
- **Related Entities:** OnboardingFlow
- **User Permissions:** Company admin access

### **State Management**
- **Local State:** Selected content block, config bar state, content order, unsaved changes
- **Global State:** Current company context, user info
- **Server State:** Stage details, content blocks

### **Responsive Considerations**
- **Mobile:** Content blocks stack vertically, config bar as bottom drawer/modal
- **Tablet:** Content blocks and config bar in single column or side-by-side
- **Desktop:** Content blocks left, config bar right

### **Accessibility Requirements**
- **Component Library:** Use accessible card, form, and sidebar components
- **Keyboard Navigation:** All interactive elements keyboard accessible
- **Screen Readers:** Proper ARIA roles for content blocks and config bar
- **Color Contrast:** High contrast for all text and interactive elements




### **Page Information**
- **Page Name:** Login
- **URL Path:** "/login"
- **User Type:** Admin
- **Purpose:** Authenticate company administrators to access the admin portal

### **Layout Structure**
```
Header: Company logo/branding (center)
Main Content:
  - Title: "Welcome Back" or "Sign In"
  - Login form (centered, card-style)
    - Email field
    - Password field
    - "Remember me" checkbox
    - "Forgot Password?" link
    - "Sign In" button
  - Footer: "Don't have an account? Sign up" link
Footer: None
```

### **Key UI Components**
- **Form:** Login form with email, password, remember me checkbox
- **Button:** "Sign In" (primary action)
- **Links:** "Forgot Password?", "Sign up" link
- **Card:** Container for the login form

### **Data Displayed**
- **Static Content:** Page title, form labels, help text
- **Dynamic Data:** Validation errors, loading states
- **User Input:** Email, password, remember me checkbox

### **User Actions & Interactions**
- **Action:** Fill out login form
  - **Trigger:** User types in form fields
  - **Frontend Request:** Local validation
  - **Expected Response:** Validation feedback
  - **UI Update:** Show validation errors
  - **Error Handling:** Inline validation errors

- **Action:** Click "Sign In" button
  - **Trigger:** Submit button
  - **Frontend Request:** POST /api/auth/login
  - **Expected Response:** Authentication token, user data
  - **UI Update:** Navigate to dashboard, store token
  - **Error Handling:** Show error toast if authentication fails

- **Action:** Click "Forgot Password?" link
  - **Trigger:** Link click
  - **Frontend Request:** Navigate to "/forgot-password"
  - **Expected Response:** Load forgot password page
  - **UI Update:** Page navigation
  - **Error Handling:** None (simple navigation)

- **Action:** Click "Sign up" link
  - **Trigger:** Link click
  - **Frontend Request:** Navigate to "/register"
  - **Expected Response:** Load registration page
  - **UI Update:** Page navigation
  - **Error Handling:** None (simple navigation)

### **API Endpoints Used**
- **POST /api/auth/login** - Authenticate user

### **Database Entities Involved**
- **Primary Entities:** User
- **Related Entities:** Company
- **User Permissions:** None (public page)

### **State Management**
- **Local State:** Form data, validation errors, loading state
- **Global State:** None (not authenticated yet)
- **Server State:** None

### **Responsive Considerations**
- **Mobile:** Form takes full width, centered
- **Tablet:** Form in card with padding
- **Desktop:** Form in centered card with shadow

### **Accessibility Requirements**
- **Component Library:** Use accessible form components
- **Keyboard Navigation:** All form fields and buttons keyboard accessible
- **Screen Readers:** Proper labels, ARIA attributes
- **Color Contrast:** High contrast for all text and interactive elements




### **Page Information**
- **Page Name:** Register
- **URL Path:** "/register"
- **User Type:** New Company Admin
- **Purpose:** Create new company account and admin user

### **Layout Structure**
```
Header: Company logo/branding (center)
Main Content:
  - Title: "Create Your Company Account"
  - Registration form (centered, card-style)
    - Company Information:
      - Company Name (required)
      - Industry (dropdown)
      - Company Size (dropdown)
      - Website (optional)
    - Admin Information:
      - First Name (required)
      - Last Name (required)
      - Email (required)
      - Password (required)
      - Confirm Password (required)
    - Terms & Conditions checkbox
    - "Create Account" button
  - Footer: "Already have an account? Sign in" link
Footer: None
```

### **Key UI Components**
- **Form:** Registration form with company and admin sections
- **Dropdowns:** Industry, Company Size
- **Button:** "Create Account" (primary action)
- **Checkbox:** Terms & Conditions
- **Links:** "Sign in" link

### **Data Displayed**
- **Static Content:** Page title, form labels, help text, terms
- **Dynamic Data:** Validation errors, loading states, dropdown options
- **User Input:** All form fields above

### **User Actions & Interactions**
- **Action:** Fill out registration form
  - **Trigger:** User types/selects in form fields
  - **Frontend Request:** Local validation
  - **Expected Response:** Validation feedback
  - **UI Update:** Show validation errors, enable/disable submit button
  - **Error Handling:** Inline validation errors

- **Action:** Click "Create Account" button
  - **Trigger:** Submit button
  - **Frontend Request:** POST /api/auth/register
  - **Expected Response:** Account created, authentication token
  - **UI Update:** Navigate to dashboard, store token
  - **Error Handling:** Show error toast if registration fails

- **Action:** Click "Sign in" link
  - **Trigger:** Link click
  - **Frontend Request:** Navigate to "/login"
  - **Expected Response:** Load login page
- **UI Update:** Page navigation
- **Error Handling:** None (simple navigation)

### **API Endpoints Used**
- **POST /api/auth/register** - Create new company and admin account
- **GET /api/industries** - Fetch industry options
- **GET /api/company-sizes** - Fetch company size options

### **Database Entities Involved**
- **Primary Entities:** Company, User
- **Related Entities:** None
- **User Permissions:** None (public page)

### **State Management**
- **Local State:** Form data, validation errors, loading state
- **Global State:** None (not authenticated yet)
- **Server State:** Industry and company size options

### **Responsive Considerations**
- **Mobile:** Form takes full width, sections stack vertically
- **Tablet:** Form in card with padding
- **Desktop:** Form in centered card with shadow

### **Accessibility Requirements**
- **Component Library:** Use accessible form components
- **Keyboard Navigation:** All form fields and buttons keyboard accessible
- **Screen Readers:** Proper labels, ARIA attributes
- **Color Contrast:** High contrast for all text and interactive elements




### **Page Information**
- **Page Name:** New Hires List
- **URL Path:** "/new-hires"
- **User Type:** Admin
- **Purpose:** View, manage, and track all new hires and their onboarding progress

### **Layout Structure**
```
Header: Company logo (left), user avatar with dropdown menu (right)
Sidebar: Navigation menu (Dashboard, Onboarding Flows, New Hires (active), Settings)
Breadcrumbs nav: Home / New Hires
Main Content:
  - Title: "New Hires"
  - Filters and Search:
    - Search bar
    - Status filter (All, Active, Completed, Pending)
    - Flow filter (dropdown)
    - Date range filter
  - Actions:
    - "Add New Hire" button
    - Bulk actions (if selected)
  - Table/List: New hires with columns (Name, Email, Assigned Flow, Progress %, Status, Start Date, Last Activity, Actions)
  - Pagination
Footer: None
```

### **Key UI Components**
- **Table/List:** New hires data (sortable, filterable)
- **Search:** Search bar for filtering
- **Filters:** Status, Flow, Date range dropdowns
- **Button:** "Add New Hire"
- **Modal:** Create/Edit new hire form
- **Actions:** Edit, Delete, View Progress for each hire
- **Pagination:** If many new hires

### **Data Displayed**
- **Static Content:** Page title, table headers, filter labels
- **Dynamic Data:**
  - List of new hires (name, email, flow, progress, status, dates)
  - Filter options (flows, statuses)
  - Search results
- **User Input:** Search text, filter selections

### **User Actions & Interactions**
- **Action:** Click "Add New Hire" button
  - **Trigger:** Button
  - **Frontend Request:** Opens new-hire modal
  - **Expected Response:** Opens modal for creating new-hire
  - **UI Update:** open modal
  - **Error Handling:** None (simple navigation)

- **Action:** Search/filter new hires
  - **Trigger:** Search input or filter selection
  - **Frontend Request:** GET /api/companies/{id}/new-hires with filters
  - **Expected Response:** Filtered new hires list
  - **UI Update:** Table updates with filtered results
  - **Error Handling:** Show error toast if API fails

- **Action:** Click on new hire row or "View Progress"
  - **Trigger:** Row click or action button
  - **Frontend Request:** Navigate to "/new-hires/{id}"
  - **Expected Response:** Load new hire detail page
  - **UI Update:** Page navigation
  - **Error Handling:** Show error toast if API fails

- **Action:** Click "Edit" action
  - **Trigger:** Action button
  - **Frontend Request:** GET /api/new-hires/{id} (fetch current data)
  - **Expected Response:** New hire data for editing
  - **UI Update:** Opens edit modal with populated form
  - **Error Handling:** Show error toast if API fails

- **Action:** Fill out new hire form in modal
  - **Trigger:** User types/selects in form fields
  - **Frontend Request:** Local validation
  - **Expected Response:** Validation feedback
  - **UI Update:** Show validation errors, enable/disable submit button
  - **Error Handling:** Inline validation errors

- **Action:** Click "Create" or "Update" button in modal
  - **Trigger:** Submit button in modal
  - **Frontend Request:** POST /api/new-hires (create) or PATCH /api/new-hires/{id} (update)
  - **Expected Response:** New hire created/updated successfully
  - **UI Update:** Modal closes, table updates, success toast
  - **Error Handling:** Show error toast if API fails

- **Action:** Click "Cancel" button in modal
  - **Trigger:** Cancel button in modal
  - **Frontend Request:** None
  - **Expected Response:** Modal closes
  - **UI Update:** Modal disappears, form resets
  - **Error Handling:** None

- **Action:** Click "Delete" action
  - **Trigger:** Action button
  - **Frontend Request:** DELETE /api/new-hires/{id}
  - **Expected Response:** New hire removed from list
  - **UI Update:** Table updates, success toast
  - **Error Handling:** Show error toast if API fails

### **API Endpoints Used**
- **GET /api/companies/{id}/new-hires** - Fetch new hires with filters
- **GET /api/new-hires/{id}** - Fetch new hire details for editing
- **POST /api/new-hires** - Create new hire
- **PATCH /api/new-hires/{id}** - Update new hire
- **DELETE /api/new-hires/{id}** - Delete new hire
- **GET /api/companies/{id}/flows** - Fetch flows for filter dropdown

### **Database Entities Involved**
- **Primary Entities:** NewHire, OnboardingFlow
- **Related Entities:** User, Progress
- **User Permissions:** Company admin access

### **State Management**
- **Local State:** Search text, filter selections, selected rows
- **Global State:** Current company context, user info
- **Server State:** New hires list, filter options

### **Responsive Considerations**
- **Mobile:** Table becomes card list, filters stack vertically
- **Tablet:** Table with horizontal scroll, filters in row
- **Desktop:** Full table visible, filters in row

### **Accessibility Requirements**
- **Component Library:** Use accessible table/list components
- **Keyboard Navigation:** All interactive elements keyboard accessible
- **Screen Readers:** Proper table semantics, ARIA labels
- **Color Contrast:** High contrast for all text and interactive elements




### **Page Information**
- **Page Name:** New Hire Detail/Progress
- **URL Path:** "/new-hires/{id}"
- **User Type:** Admin
- **Purpose:** View detailed information and progress of a specific new hire

### **Layout Structure**
```
Header: Company logo (left), user avatar with dropdown menu (right)
Sidebar: Navigation menu (Dashboard, Onboarding Flows, New Hires (active), Settings)
Breadcrumbs nav: Home / New Hires / [New Hire Name]
Main Content:
  - Header: New hire info (name, email, assigned flow, status)
  - Tabs:
    1. Progress (default active):
      - Progress overview (completion percentage, time remaining)
      - Stage-by-stage progress (cards showing each stage status)
      - Timeline view of completed activities
    2. Details:
      - Personal information
      - Assigned flow details
      - Start date, expected completion
      - Notes/comments section
    3. Activity:
      - Log of all activities and interactions
      - Form submissions, stage completions, etc.
  - Actions: Edit, Resend Invitation, Mark Complete, etc.
Footer: None
```

### **Key UI Components**
- **Tabs:** Progress, Details, Activity
- **Progress Cards:** Stage-by-stage progress visualization
- **Timeline:** Activity timeline
- **Info Cards:** Personal and flow information
- **Actions:** Edit, resend invitation, mark complete buttons

### **Data Displayed**
- **Static Content:** Section headers, tab labels
- **Dynamic Data:**
  - New hire details (name, email, personal info)
  - Assigned flow information
  - Progress data (completion %, stage status)
  - Activity log
  - Timeline events

### **User Actions & Interactions**
- **Action:** Switch tabs
  - **Trigger:** Tab click
  - **Frontend Request:** None (local state)
  - **Expected Response:** Show selected tab content
  - **UI Update:** Tab content changes
  - **Error Handling:** None

- **Action:** Click "Edit" button
  - **Trigger:** Edit button
  - **Frontend Request:** Navigate to "/new-hires/{id}/edit"
  - **Expected Response:** Load edit page
  - **UI Update:** Page navigation
  - **Error Handling:** Show error toast if API fails

- **Action:** Click "Resend Invitation"
  - **Trigger:** Resend button
  - **Frontend Request:** POST /api/new-hires/{id}/resend-invitation
  - **Expected Response:** Invitation sent successfully
  - **UI Update:** Success toast
  - **Error Handling:** Show error toast if API fails

- **Action:** Click "Mark Complete"
  - **Trigger:** Complete button
  - **Frontend Request:** PATCH /api/new-hires/{id}/status (complete)
  - **Expected Response:** Status updated
  - **UI Update:** Status changes, success toast
  - **Error Handling:** Show error toast if API fails

### **API Endpoints Used**
- **GET /api/new-hires/{id}** - Fetch new hire details
- **GET /api/new-hires/{id}/progress** - Fetch progress data
- **GET /api/new-hires/{id}/activity** - Fetch activity log
- **POST /api/new-hires/{id}/resend-invitation** - Resend invitation
- **PATCH /api/new-hires/{id}/status** - Update status

### **Database Entities Involved**
- **Primary Entities:** NewHire, Progress
- **Related Entities:** OnboardingFlow, Stage, User
- **User Permissions:** Company admin access

### **State Management**
- **Local State:** Active tab, selected actions
- **Global State:** Current company context, user info
- **Server State:** New hire details, progress data, activity log

### **Responsive Considerations**
- **Mobile:** Tabs stack vertically, progress cards in single column
- **Tablet:** Tabs and cards in 2-column layout
- **Desktop:** Tabs and cards in multi-column layout

### **Accessibility Requirements**
- **Component Library:** Use accessible tab and card components
- **Keyboard Navigation:** All interactive elements keyboard accessible
- **Screen Readers:** Proper ARIA roles for tabs, cards, timeline
- **Color Contrast:** High contrast for all text and interactive elements




### **Page Information**
- **Page Name:** Company Settings
- **URL Path:** "/settings"
- **User Type:** Admin
- **Purpose:** Manage company profile, branding, subscription, and account settings

### **Layout Structure**
```
Header: Company logo (left), user avatar with dropdown menu (right)
Sidebar: Navigation menu (Dashboard, Onboarding Flows, New Hires, Settings (active))
Breadcrumbs nav: Home / Settings
Main Content:
  - Title: "Company Settings"
  - Tabs:
    1. Company Profile (default active):
      - Company Name
      - Industry
      - Company Size
      - Website
      - Description
    2. Branding:
      - Logo upload
      - Primary Color
      - Secondary Color
      - Accent Color
      - Preview section
    3. Subscription & Billing:
      - Current plan
      - Usage statistics
      - Billing information
      - Payment methods
    4. Account Settings:
      - Admin user management
      - Security settings
      - Notification preferences
  - Save button for each section
Footer: None
```

### **Key UI Components**
- **Tabs:** Company Profile, Branding, Subscription & Billing, Account Settings
- **Forms:** Company info, branding settings, billing info
- **File Upload:** Logo upload with preview
- **Color Pickers:** Primary, secondary, accent colors
- **Buttons:** Save for each section
- **Preview:** Branding preview section

### **Data Displayed**
- **Static Content:** Section headers, tab labels, help text
- **Dynamic Data:**
  - Company information
  - Current branding settings
  - Subscription and billing details
  - Admin users list
- **User Input:** All form fields, file uploads

### **User Actions & Interactions**
- **Action:** Switch tabs
  - **Trigger:** Tab click
  - **Frontend Request:** None (local state)
  - **Expected Response:** Show selected tab content
  - **UI Update:** Tab content changes
  - **Error Handling:** None

- **Action:** Edit company profile
  - **Trigger:** Form field changes
  - **Frontend Request:** None (local state)
  - **Expected Response:** Form validation feedback
  - **UI Update:** Show validation errors
  - **Error Handling:** Inline validation errors

- **Action:** Upload logo
  - **Trigger:** File upload
  - **Frontend Request:** POST /api/companies/{id}/logo
  - **Expected Response:** Logo uploaded successfully
  - **UI Update:** Logo preview updates
  - **Error Handling:** Show error toast if upload fails

- **Action:** Change branding colors
  - **Trigger:** Color picker selection
  - **Frontend Request:** None (local state)
  - **Expected Response:** Preview updates
  - **UI Update:** Branding preview updates
  - **Error Handling:** None

- **Action:** Click "Save" button
  - **Trigger:** Save button
  - **Frontend Request:** PATCH /api/companies/{id} (section-specific data)
  - **Expected Response:** Settings saved successfully
  - **UI Update:** Success toast
- **Error Handling:** Show error toast if API fails

### **API Endpoints Used**
- **GET /api/companies/{id}** - Fetch company settings
- **PATCH /api/companies/{id}** - Update company settings
- **POST /api/companies/{id}/logo** - Upload company logo
- **GET /api/companies/{id}/subscription** - Fetch subscription details

### **Database Entities Involved**
- **Primary Entities:** Company
- **Related Entities:** User, Subscription
- **User Permissions:** Company admin access

### **State Management**
- **Local State:** Active tab, form data, unsaved changes
- **Global State:** Current company context, user info
- **Server State:** Company settings, subscription data

### **Responsive Considerations**
- **Mobile:** Tabs stack vertically, forms in single column
- **Tablet:** Tabs and forms in 2-column layout
- **Desktop:** Tabs and forms in multi-column layout

### **Accessibility Requirements**
- **Component Library:** Use accessible tab and form components
- **Keyboard Navigation:** All interactive elements keyboard accessible
- **Screen Readers:** Proper ARIA roles for tabs, forms, file upload
- **Color Contrast:** High contrast for all text and interactive elements


<!-- New Hire Onboarding Landing Page -->

### **Page Information**
- **Page Name:** New Hire Onboarding Landing
- **URL Path:** "/onboarding/{sessionId}" or custom subdomain
- **User Type:** New Hire
- **Purpose:** Welcome page for new hires to start their onboarding process

### **Layout Structure**
```
Header: Company logo and branding (centered)
Main Content:
  - Welcome section:
    - Personalized greeting (e.g., "Welcome, [Name]!")
    - Company name and branding
    - Brief description of onboarding process
  - Onboarding info:
    - Estimated duration
    - Number of stages
    - What to expect
  - Action buttons:
    - "Start Onboarding" (primary)
    - "Resume Onboarding" (if in progress)
  - Support info:
    - Contact information
    - Help resources
Footer: Company branding and links
```

### **Key UI Components**
- **Welcome Card:** Personalized greeting and company info
- **Info Cards:** Duration, stages, expectations
- **Buttons:** Start/Resume onboarding
- **Support Section:** Contact info, help links
- **Progress Indicator:** If onboarding was started before

### **Data Displayed**
- **Static Content:** Welcome message, company branding
- **Dynamic Data:**
  - New hire name and personal info
  - Assigned onboarding flow details
  - Progress status (if started)
  - Company branding and colors
- **User Input:** Button clicks

### **User Actions & Interactions**
- **Action:** Click "Start Onboarding" button
  - **Trigger:** Start button
  - **Frontend Request:** POST /api/onboarding/{sessionId}/start
  - **Expected Response:** Onboarding started, first stage data
  - **UI Update:** Navigate to first onboarding step
  - **Error Handling:** Show error toast if API fails

- **Action:** Click "Resume Onboarding" button
  - **Trigger:** Resume button
  - **Frontend Request:** GET /api/onboarding/{sessionId}/progress
  - **Expected Response:** Current progress and next stage
  - **UI Update:** Navigate to current stage
  - **Error Handling:** Show error toast if API fails

- **Action:** Click support links
  - **Trigger:** Support link clicks
  - **Frontend Request:** Navigate to support resources
  - **Expected Response:** Load support page or open contact
  - **UI Update:** Page navigation or modal
  - **Error Handling:** None

### **API Endpoints Used**
- **GET /api/onboarding/{sessionId}** - Fetch onboarding session details
- **POST /api/onboarding/{sessionId}/start** - Start onboarding
- **GET /api/onboarding/{sessionId}/progress** - Get current progress

### **Database Entities Involved**
- **Primary Entities:** NewHire, OnboardingSession
- **Related Entities:** OnboardingFlow, Company
- **User Permissions:** None (public page with session token)

### **State Management**
- **Local State:** Session token, onboarding status
- **Global State:** None (new hire context)
- **Server State:** Onboarding session, flow details

### **Responsive Considerations**
- **Mobile:** Single column layout, full-width buttons
- **Tablet:** Centered content with padding
- **Desktop:** Centered content with max-width

### **Accessibility Requirements**
- **Component Library:** Use accessible card and button components
- **Keyboard Navigation:** All interactive elements keyboard accessible
- **Screen Readers:** Proper heading hierarchy, ARIA labels
- **Color Contrast:** High contrast for all text and interactive elements


<!-- Dynamic Onboarding Step Page -->

### **Page Information**
- **Page Name:** Onboarding Step
- **URL Path:** "/onboarding/{sessionId}/step/{stepId}"
- **User Type:** New Hire
- **Purpose:** Display individual onboarding stage content and collect user input

### **Layout Structure**
```
Header: Company logo and branding (left), progress indicator (right)
Progress Bar: Top of page showing overall progress and current stage
Main Content:
  - Stage title and description
  - Dynamic content area (renders based on content type):
    - Text content
    - Media (images, videos)
    - Forms (inputs, checkboxes, file uploads)
    - External links
    - Checklists
    - etc.
  - Navigation:
    - "Previous" button (if not first stage)
    - "Next" button (if not last stage)
    - "Complete" button (if last stage)
Footer: Support info and company branding
```

### **Key UI Components**
- **Progress Bar:** Overall progress and current stage indicator
- **Content Renderer:** Dynamic content based on stage type
- **Form Components:** Various input types (text, file, checkbox, etc.)
- **Navigation:** Previous/Next/Complete buttons
- **Media Player:** For video/image content
- **File Upload:** For document uploads

### **Data Displayed**
- **Static Content:** Stage title, navigation buttons
- **Dynamic Data:**
  - Stage content (text, media, forms)
  - Progress information
  - Form validation
  - User input responses
- **User Input:** All form fields, file uploads, checkboxes

### **User Actions & Interactions**
- **Action:** Fill out form fields
  - **Trigger:** User input in form fields
  - **Frontend Request:** Local validation
  - **Expected Response:** Validation feedback
  - **UI Update:** Show validation errors, enable/disable next button
  - **Error Handling:** Inline validation errors

- **Action:** Upload files
  - **Trigger:** File upload
  - **Frontend Request:** POST /api/onboarding/{sessionId}/uploads
  - **Expected Response:** File uploaded successfully
  - **UI Update:** File preview, progress indicator
  - **Error Handling:** Show error toast if upload fails

- **Action:** Click "Next" button
  - **Trigger:** Next button
  - **Frontend Request:** POST /api/onboarding/{sessionId}/steps/{stepId}/complete
  - **Expected Response:** Stage completed, next stage data
  - **UI Update:** Navigate to next stage, update progress
  - **Error Handling:** Show error toast if API fails

- **Action:** Click "Previous" button
  - **Trigger:** Previous button
  - **Frontend Request:** Navigate to previous stage
  - **Expected Response:** Previous stage data
  - **UI Update:** Navigate to previous stage
  - **Error Handling:** None (simple navigation)

- **Action:** Click "Complete" button (final stage)
  - **Trigger:** Complete button
  - **Frontend Request:** POST /api/onboarding/{sessionId}/complete
  - **Expected Response:** Onboarding completed
  - **UI Update:** Navigate to completion page
  - **Error Handling:** Show error toast if API fails

### **API Endpoints Used**
- **GET /api/onboarding/{sessionId}/steps/{stepId}** - Fetch stage content
- **POST /api/onboarding/{sessionId}/steps/{stepId}/complete** - Complete stage
- **POST /api/onboarding/{sessionId}/uploads** - Upload files
- **POST /api/onboarding/{sessionId}/complete** - Complete onboarding

### **Database Entities Involved**
- **Primary Entities:** OnboardingSession, Stage, ContentBlock
- **Related Entities:** NewHire, Progress
- **User Permissions:** None (public page with session token)

### **State Management**
- **Local State:** Form data, validation errors, file uploads
- **Global State:** Session token, progress
- **Server State:** Stage content, progress data

### **Responsive Considerations**
- **Mobile:** Single column, full-width content, stacked buttons
- **Tablet:** Centered content with padding
- **Desktop:** Centered content with max-width

### **Accessibility Requirements**
- **Component Library:** Use accessible form and media components
- **Keyboard Navigation:** All interactive elements keyboard accessible
- **Screen Readers:** Proper form labels, ARIA attributes for media
- **Color Contrast:** High contrast for all text and interactive elements