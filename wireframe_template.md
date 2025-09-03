# Wireframe Template for Onboarding-as-a-Service

## Template Instructions

Use this template to describe each page/screen of your application. For each page, fill out all sections that apply. This structured approach will help translate wireframes into backend API endpoints and database models.

---

## Page Template

### **Page Information**
- **Page Name:** [e.g., "Company Admin Dashboard", "New Hire Onboarding Step 1"]
- **URL Path:** [e.g., "/dashboard", "/onboarding/step1"]
- **User Type:** [Admin/New Hire]
- **Purpose:** [Brief description of what this page does]

### **Layout Structure**
```
Header: [Describe header elements - logo, navigation, user menu, etc.]
Sidebar: [If applicable - navigation menu, filters, etc.]
Main Content: [Describe the main content area layout]
Footer: [If applicable - links, copyright, etc.]
```

### **Key UI Components**
- **Forms:** [List form fields, validation rules, submit actions]
- **Tables/Lists:** [Describe data columns, sorting, filtering, pagination]
- **Cards:** [Describe card content, actions, status indicators]
- **Modals/Dialogs:** [Describe popup content, triggers, actions]
- **Navigation:** [Describe menu items, breadcrumbs, pagination]

### **Data Displayed**
- **Static Content:** [Text, images, help content]
- **Dynamic Data:** [Data fetched from APIs - lists, counts, statuses]
- **User Input:** [Forms, file uploads, selections]

### **User Actions & Interactions**
For each user action, specify:
- **Action:** [What user does - click, type, select, etc.]
- **Trigger:** [What element triggers this action]
- **Frontend Request:** [What data is sent to backend]
- **Expected Response:** [What data comes back]
- **UI Update:** [How the UI changes after action]
- **Error Handling:** [What happens if action fails]

### **API Endpoints Used**
- **GET Requests:** [List all data fetching endpoints]
- **POST Requests:** [List all data creation endpoints]
- **PUT/PATCH Requests:** [List all data update endpoints]
- **DELETE Requests:** [List all data deletion endpoints]

### **Database Entities Involved**
- **Primary Entities:** [Main data entities this page works with]
- **Related Entities:** [Connected entities that might be displayed]
- **User Permissions:** [What permissions are needed to access this page]

### **State Management**
- **Local State:** [Component-level state - form data, UI toggles]
- **Global State:** [App-level state - user info, company context]
- **Server State:** [Data fetched from APIs - cached vs real-time]

### **Responsive Considerations**
- **Mobile:** [How layout adapts for mobile]
- **Tablet:** [How layout adapts for tablet]
- **Desktop:** [How layout adapts for desktop]

### **Accessibility Requirements**
- **Keyboard Navigation:** [How keyboard users interact]
- **Screen Readers:** [ARIA labels, semantic HTML]
- **Color Contrast:** [Any specific color requirements]

---

## Example Completed Template

### **Page Information**
- **Page Name:** Company Admin Dashboard
- **URL Path:** "/dashboard"
- **User Type:** Admin
- **Purpose:** Overview of company's onboarding activities and quick access to key features

### **Layout Structure**
```
Header: Company logo (left), user avatar with dropdown menu (right)
Sidebar: Navigation menu with icons and labels
  - Dashboard (active)
  - Onboarding Flows
  - New Hires
  - Settings
Main Content: Grid of dashboard cards and recent activity list
Footer: None
```

### **Key UI Components**
- **Cards:** 4 dashboard cards showing stats (Active Flows, New Hires This Month, Completion Rate, Recent Activity)
- **Table:** Recent new hires with columns (Name, Assigned Flow, Progress %, Last Activity)
- **Button:** "Create New Flow" CTA button
- **Search:** Search bar for filtering new hires

### **Data Displayed**
- **Static Content:** Page title "Dashboard", card titles
- **Dynamic Data:** 
  - Dashboard stats (counts, percentages)
  - Recent new hires list
  - Company name and branding

### **User Actions & Interactions**
- **Action:** Click "Create New Flow" button
- **Trigger:** CTA button in main content area
- **Frontend Request:** Navigate to "/flows/create"
- **Expected Response:** Load flow creation page
- **UI Update:** Page navigation
- **Error Handling:** None (simple navigation)

- **Action:** Click on new hire row
- **Trigger:** Table row click
- **Frontend Request:** GET /api/new-hires/{id}
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
- **Desktop:** Cards in 2x2 grid, full sidebar visible

### **Accessibility Requirements**
- **Keyboard Navigation:** All interactive elements keyboard accessible
- **Screen Readers:** Proper heading hierarchy, alt text for stats
- **Color Contrast:** High contrast for all text and interactive elements

---

## Page List to Complete

### **Company Admin Portal**
1. Login Page
2. Dashboard
3. Onboarding Flows List
4. Create/Edit Onboarding Flow
5. New Hires List
6. New Hire Detail/Progress
7. Company Settings
8. Register Page

### **New Hire Portal**
1. Onboarding Landing Page
2. Onboarding Step Pages (for each stage type)
3. Progress/Summary Page
4. Completion Page

### **Shared Pages**
1. Error Pages (404, 500)
2. Loading States
3. Success/Confirmation Pages

---

## Notes for Completion

- Be specific about data types and validation rules
- Include all possible user interactions, not just happy path
- Consider error states and edge cases
- Think about data relationships and dependencies
- Consider performance implications of data fetching
- Include any business rules or constraints 