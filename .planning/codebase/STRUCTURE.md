# Codebase Structure

**Analysis Date:** 2026-02-03

## Directory Layout

```
forms-flow-ai-micro-front-ends/
├── forms-flow-admin/          # Admin dashboard (dashboard, role, user management)
│   └── src/
│       ├── components/        # React UI components (footer, manage, etc.)
│       ├── containers/        # Container components
│       ├── services/          # Admin-specific services
│       ├── endpoints/         # Config and API endpoints
│       ├── constants/         # Feature flags and constants
│       ├── utils/             # Helper functions
│       ├── resourceBundles/   # i18n translations
│       ├── index.tsx          # Main component with routing
│       ├── formsflow-admin.tsx  # Single-spa entry point
│       ├── root.component.tsx # Root wrapper
│       └── root.component.test.tsx
├── forms-flow-nav/            # Navigation bar and routing orchestration
│   └── src/
│       ├── sidenav/           # Sidebar navigation components
│       ├── services/          # Navigation services (language, tenant, integration)
│       ├── helper/            # Helper utilities
│       ├── endpoints/         # Config endpoints
│       ├── constants/         # User roles, feature flags
│       ├── resourceBundles/   # i18n translations
│       ├── Navbar.jsx         # Main navbar component
│       ├── Navbar.scss        # Navbar styles
│       ├── formsflow-nav.js   # Single-spa entry point
│       ├── root.component.js  # Root wrapper
│       └── variables.scss     # SCSS variables
├── forms-flow-service/        # Shared services library
│   └── src/
│       ├── keycloak/          # Keycloak authentication service
│       ├── storage/           # StorageService (localStorage/sessionStorage)
│       ├── request/           # RequestService (axios wrapper)
│       ├── apiManager/        # API request managers for specific domains
│       ├── routerServices/    # Router constants and navigation helpers
│       ├── helpers/           # Utility helpers (style, compact form, etc.)
│       ├── resourceBundles/   # i18n base and formio translations
│       ├── constants/         # Shared constants
│       └── formsflow-services.ts  # Main export file (public API)
├── forms-flow-components/     # Reusable component library
│   └── src/
│       ├── components/        # React components (CustomComponents, SvgImages, SvgIcons)
│       ├── customHooks/       # Custom React hooks
│       ├── service/           # Component services (PDF export, etc.)
│       ├── api/               # Component API utilities
│       ├── constants/         # Component constants
│       ├── helper/            # Component helpers
│       ├── resourceBundles/   # i18n translations
│       ├── mocks/             # Jest mocks
│       ├── __test__/          # Unit tests
│       └── formsflow-components.ts  # Main export file (public API)
├── forms-flow-theme/          # Global theming and styling
│   └── scss/
│       ├── v8-scss/           # Bootstrap 5 theme overrides
│       ├── utils/             # SCSS utilities and mixins
│       └── external/          # External library overrides
├── forms-flow-review/         # Task review/management application
│   └── src/
│       ├── components/        # React components (task list, task detail, filters, etc.)
│       ├── Routes/            # Route-level components (TaskListing, TaskDetails)
│       ├── actions/           # Redux actions (taskActions, tenantActions)
│       ├── reducers/          # Redux reducers (taskReducer, customSubmissionReducer, etc.)
│       ├── services/          # Services (SocketIOService, StoreService)
│       ├── api/               # API endpoints and services
│       │   ├── services/      # Domain-specific API calls
│       │   ├── config.ts      # API configuration
│       │   └── endpoints.ts   # API endpoint constants
│       ├── types/             # TypeScript type definitions
│       ├── config/            # i18n configuration
│       ├── constants/         # Constants and feature flags
│       ├── resourceBundles/   # i18n translations
│       ├── helper/            # Utility helpers
│       ├── __tests__/         # Unit tests
│       ├── index.tsx          # Main component with Redux setup and auth
│       ├── formsflow-review.tsx   # Single-spa entry point
│       ├── root.component.tsx # Root wrapper with Redux provider
│       └── index.scss         # Main stylesheet
├── forms-flow-submissions/    # Submission analysis application
│   └── src/
│       ├── components/        # React components
│       ├── Routes/            # Route-level components
│       ├── actions/           # Redux actions
│       ├── reducers/          # Redux reducers
│       ├── services/          # Services (StoreService, etc.)
│       ├── api/               # API endpoints and services
│       │   ├── services/      # Domain-specific API calls
│       │   ├── config.ts      # API configuration
│       │   └── endpoints.ts   # API endpoint constants
│       ├── types/             # TypeScript type definitions
│       ├── config/            # Configuration
│       ├── constants/         # Constants
│       ├── resourceBundles/   # i18n translations
│       ├── helper/            # Utility helpers
│       ├── __tests__/         # Unit tests
│       ├── index.tsx          # Main component
│       ├── formsflow-submissions.tsx  # Single-spa entry point
│       ├── root.component.tsx # Root wrapper with Redux and React Query providers
│       └── index.scss         # Main stylesheet
├── forms-flow-integration/    # Integration configuration application
│   └── src/
│       ├── components/        # React components
│       ├── containers/        # Container components
│       ├── services/          # Integration services
│       ├── endpoints/         # Config and API endpoints
│       ├── constants/         # Constants
│       ├── resourceBundles/   # i18n translations
│       ├── index.tsx          # Main component
│       ├── formsflow-integration.tsx  # Single-spa entry point
│       └── root.component.tsx # Root wrapper
└── scripts/                   # Build and utility scripts
```

## Directory Purposes

**forms-flow-admin:**
- Purpose: Admin-only features for dashboard, role, and user management
- Key files: `src/components/Manage.tsx`, `src/components/manage/DashboardManagement.tsx`
- Roles required: manage_dashboard_authorizations, manage_roles, manage_users

**forms-flow-nav:**
- Purpose: Navigation bar, routing orchestration, language switching, tenant awareness
- Key files: `src/Navbar.jsx`, `src/sidenav/Sidenav.jsx`
- Loaded by: Root config (available to all authenticated users)

**forms-flow-service:**
- Purpose: Centralized shared logic and APIs for all micro-frontends
- Key exports: KeycloakService, StorageService, RequestService, navigation helpers
- Not a micro-frontend; consumed as npm package @formsflow/service

**forms-flow-components:**
- Purpose: Reusable UI components and patterns
- Key exports: CustomComponents, SvgIcons, custom hooks
- Not a micro-frontend; consumed as npm package @formsflow/components

**forms-flow-theme:**
- Purpose: Global CSS variables and theme overrides
- Key files: `scss/v8-scss/variables.scss` (CSS custom properties)
- Imported by: All modules via index.scss

**forms-flow-review:**
- Purpose: Task review, assignment, filtering for staff reviewers
- Roles required: view_tasks, manage_tasks, manage_all_filters
- State: Redux store with task list, filters, form data

**forms-flow-submissions:**
- Purpose: Submission analysis and reporting
- Roles required: view_submissions
- State: Redux store with submission lists, applications, bundles
- Extra: React Query for async data fetching

**forms-flow-integration:**
- Purpose: Configuration of external integrations
- Roles required: integration management roles
- Key features: Connected apps, integration recipes, library

## Key File Locations

**Entry Points:**

- `forms-flow-admin/src/formsflow-admin.tsx`: Single-spa lifecycle for admin module
- `forms-flow-nav/src/formsflow-nav.js`: Single-spa lifecycle for nav module
- `forms-flow-review/src/formsflow-review.tsx`: Single-spa lifecycle for review module
- `forms-flow-submissions/src/formsflow-submissions.tsx`: Single-spa lifecycle for submissions module
- `forms-flow-components/src/formsflow-components.ts`: Library export
- `forms-flow-service/src/formsflow-services.ts`: Library export

**Configuration:**

- `forms-flow-review/src/api/config.ts`: API URLs, Keycloak config for review module
- `forms-flow-submissions/src/api/config.ts`: API URLs, Keycloak config for submissions module
- `forms-flow-service/src/constants/`: Shared constants (MULTITENANCY_ENABLED, etc.)
- `forms-flow-theme/scss/v8-scss/variables.scss`: CSS variables for theming

**Core Logic:**

- `forms-flow-service/src/keycloak/KeycloakService.ts`: Authentication and token management
- `forms-flow-service/src/storage/storageService.ts`: Storage API with key constants
- `forms-flow-service/src/request/requestService.ts`: HTTP client with interceptors
- `forms-flow-review/src/services/StoreService.ts`: Redux store configuration
- `forms-flow-submissions/src/services/StoreServices.ts`: Redux store configuration

**Testing:**

- `forms-flow-components/src/__test__/`: Jest tests for components
- `forms-flow-review/src/__tests__/`: Jest tests for review module
- `forms-flow-submissions/src/__tests__/`: Jest tests for submissions module
- `forms-flow-components/.storybook/`: Storybook configuration for visual testing
- `forms-flow-components/__mocks__/@formsflow/`: Jest mocks for service imports

## Naming Conventions

**Files:**

- React components: PascalCase with `.tsx` or `.jsx` extension (e.g., `Navbar.jsx`, `TaskList.tsx`)
- Services: camelCase with Service suffix (e.g., `storageService.ts`, `StoreService.ts`)
- Actions/Reducers: camelCase with suffix (e.g., `taskActions.ts`, `taskReducer.ts`)
- Styles: `index.scss` co-located with component or `Navbar.scss` matching component name
- Constants: UPPER_SNAKE_CASE in constants.ts files
- Test files: `.test.tsx` or `.spec.tsx` suffix

**Directories:**

- Feature directories: kebab-case (e.g., `forms-flow-review`, `forms-flow-submissions`)
- Internal structure: camelCase (e.g., `components`, `resourceBundles`, `customHooks`)
- Domain grouping: plural nouns (e.g., `components`, `services`, `reducers`, `actions`)

## Where to Add New Code

**New Feature (within a module):**

- Primary code: Create directory under `src/components/FeatureName/` for components, `src/actions/` for Redux actions
- Tests: `src/__tests__/FeatureName.test.tsx`
- Styles: Co-locate SCSS file with component directory or in `src/styles/`
- Types: Add interfaces to `src/types/` or inline in component file
- i18n: Add keys to `src/resourceBundles/en.json` and other language files

**Example for new task filter in forms-flow-review:**

```
forms-flow-review/src/
├── components/
│   └── TaskFilter/         # New component directory
│       ├── TaskFilter.tsx  # Component implementation
│       ├── TaskFilter.scss # Component styles
│       └── TaskFilter.test.tsx
├── actions/
│   └── taskFilterActions.ts  # Redux actions for filter
├── reducers/
│   └── taskFilterReducer.ts  # Redux reducer (or extend taskReducer)
└── resourceBundles/
    ├── en.json  # Add filter-related keys
    └── fr.json
```

**New Component Library Component:**

- Implementation: `forms-flow-components/src/components/ComponentName/ComponentName.tsx`
- Styles: `forms-flow-components/src/components/ComponentName/ComponentName.scss`
- Storybook: `forms-flow-components/src/components/ComponentName/ComponentName.stories.tsx`
- Tests: `forms-flow-components/src/__test__/ComponentName.test.tsx`
- Export: Add to `forms-flow-components/src/components/index.ts`

**New Service (shared across modules):**

- Implementation: `forms-flow-service/src/newFeature/newFeatureService.ts`
- Export: Add export to `forms-flow-service/src/formsflow-services.ts`
- Tests: Co-locate as `.test.ts` files

**New API Endpoint:**

1. Add URL to `src/api/endpoints.ts` in the module (e.g., `forms-flow-review/src/api/endpoints.ts`)
2. Create service function in `src/api/services/domainServices.ts` calling RequestService
3. Create Redux action/thunk if needed (review/submissions modules)
4. Call service from component or Redux middleware

**Utilities & Helpers:**

- Shared helpers: `forms-flow-service/src/helpers/`
- Module-specific: `src/helper/` within each module (e.g., `forms-flow-review/src/helper/`)
- Custom hooks: `forms-flow-components/src/customHooks/` for reusable; `src/hooks/` within module for local

## Special Directories

**forms-flow-components/__mocks__/@formsflow/:**
- Purpose: Jest mock implementations for @formsflow/service imports
- Generated: No, hand-created
- Committed: Yes
- Usage: Auto-resolved by Jest when tests import @formsflow/service

**forms-flow-components/.storybook/:**
- Purpose: Storybook configuration and setup
- Generated: Partially (stories auto-discovered)
- Committed: Yes
- Usage: Runs at `npm run storybook` for component documentation

**forms-flow-theme/scss/:**
- Purpose: Global CSS variables and theme system
- Generated: No
- Committed: Yes
- Usage: Imported first in each module's root stylesheet to make variables available

**node_modules/ (implicit):**
- Purpose: Dependencies installed by npm
- Generated: Yes (from package-lock.json)
- Committed: No

**dist/ (implicit):**
- Purpose: Build output from webpack
- Generated: Yes (by `npm run build`)
- Committed: No

---

*Structure analysis: 2026-02-03*
