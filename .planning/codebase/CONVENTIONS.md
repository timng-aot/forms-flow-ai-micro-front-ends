# Coding Conventions

**Analysis Date:** 2026-02-03

## Naming Patterns

**Files:**
- Component files: `ComponentName.tsx` (PascalCase) - Example: `Button.tsx`, `CustomButton.tsx`, `ErrorModal.tsx`
- Hook files: `useHookName.ts` (camelCase with use prefix)
- Service files: `functionName.ts` (camelCase) - Examples: `users/index.ts`, `roles/index.ts`
- Utility/Helper files: `helpers.ts`, `utils.ts` (lowercase, descriptive)
- Test files: `ComponentName.test.tsx` or co-located in `__test__` directory - Examples: `button.test.tsx`, `MultiSelect.test.tsx`
- Barrel files: `index.tsx` or `index.ts` for component/module exports

**Functions:**
- Component functions: PascalCase - Examples: `Root`, `Users`, `CustomButton`
- Regular functions/handlers: camelCase - Examples: `handleSearch`, `removePermission`, `getButtonClassName`, `addUserPermission`
- Utility functions: camelCase - Examples: `removingTenantId`, `getRedirectUrl`, `updateMenuStyle`

**Variables:**
- State variables: camelCase - Examples: `selectedRow`, `selectedRoles`, `roleNameMapper`, `searchKey`
- Constants: SCREAMING_SNAKE_CASE - Examples: `KEYCLOAK_ENABLE_CLIENT_AUTH`, `MULTITENANCY_ENABLED`
- React hooks: camelCase with use prefix - Examples: `useTranslation()`, `useHistory()`, `useParams()`
- Objects/data: camelCase - Examples: `sizeClassMap`, `roleNameMapper`

**Types:**
- Interface names: PascalCase - Example: `CustomButtonProps`, `DropdownItem`
- Type aliases: PascalCase
- Props interfaces: `ComponentNameProps` - Example: `CustomButtonProps`

## Code Style

**Formatting:**
- Prettier v2.3.2 is used for code formatting
- Command: `prettier --write .` (in each package)
- Check format: `prettier --check .`

**Linting:**
- ESLint v7.32.0 with ts-react-important-stuff config
- Command: `eslint src --ext js,ts,tsx`
- Config location: `.eslintrc` in each package root
- Config extends: `ts-react-important-stuff` + `plugin:prettier/recommended`
- Parser: `@babel/eslint-parser` with `requireConfigFile: false`

**TypeScript:**
- Version: 4.3.5
- JSX: `react-jsx` (not React.createElement)
- Declaration output: `declarationDir: dist`
- Tests excluded from compilation
- Configuration: `tsconfig.json` extends `ts-config-single-spa`

## Import Organization

**Order:**
1. External libraries (React, third-party packages)
2. Internal imports from parent/sibling modules
3. Relative imports from local utilities/services
4. Style imports (SCSS/CSS)

**Pattern:**
```typescript
import React from "react";
import { useTranslation } from "react-i18next";
import { Translation } from "react-i18next";
import Button from "react-bootstrap/Button";
import Loading from "../loading";
import { AddUserRole, RemoveUserRole } from "../../services/users";
import { KEYCLOAK_ENABLE_CLIENT_AUTH } from "../../constants";
import { TableFooter, CustomSearch } from "@formsflow/components";
import { navigateToAdminUsers } from "@formsflow/service";
import "./users.scss";
```

**Path Aliases:**
- `@formsflow/components` - imports from forms-flow-components package
- `@formsflow/service` - imports from forms-flow-service package
- Relative paths for same-package imports

## Error Handling

**Patterns:**
- Promise-based error handling with `.catch()` for async operations
- Callback-based error handling for service functions (error handler callback)
- `try-catch` for synchronous operations (used sparingly)

**Service Layer Pattern:**
```typescript
export const fetchUsers = (
  group: string | null,
  pageNo: number | null,
  search: string | null,
  callback: any,
  errorHandler: any
) => {
  RequestService.httpGETRequest(url)
    .then((res) => {
      if (res.data) {
        callback(res.data);
      } else {
        errorHandler("No Users found!");
      }
    })
    .catch((error) => {
      if (error?.response?.data) {
        errorHandler(error.response.data?.message);
      } else {
        errorHandler("Failed to fetch users!");
      }
    });
};
```

**Component Error Handling:**
- State-based error tracking: `const [error, setError] = React.useState(null);`
- Error passed through props to service callbacks
- User notifications via `toast.error()` from react-toastify

## Logging

**Framework:** `console` object (browser native)

**Patterns:**
- `console.log()` for debug information
- `console.error()` for error logging - Example: `console.error("Error calculating days difference:", error);`
- Minimal logging; primarily used for debugging specific issues
- No structured logging framework observed

**Guidelines:**
- Use error logging in catch blocks
- Log only in development/debugging scenarios
- Avoid logging sensitive data

## Comments

**When to Comment:**
- Inline comments for bug fixes or non-obvious logic
- Comments for import corrections or clarifications
- Comments explaining why a particular implementation was chosen

**Examples from codebase:**
```typescript
// Import Modal from react-bootstrap
import Modal from "react-bootstrap/Modal";

// Initialize error state with null instead of undefined
const [error, setError] = React.useState(null);

// Corrected the function name from setROleNameMapper to setRoleNameMapper
setRoleNameMapper(mapper);

// Add state for managing invite modal
const [showInviteModal, setShowInviteModal] = React.useState(false);

// Error calculating days difference
console.error("Error calculating days difference:", error);
```

**JSDoc/TSDoc:**
- Not systematically used
- TypeScript interfaces provide implicit documentation
- Props interfaces (e.g., `CustomButtonProps`) serve as self-documentation

## Function Design

**Size:**
- Medium-sized functions (50-150 lines typical)
- Larger components broken into smaller handlers (e.g., `removePermission`, `addUserPermission`)
- Extracted utility functions for repeated logic

**Parameters:**
- Named parameters with types for services
- Props objects for React components
- Callback and error handler pattern: `callback: any, errorHandler: any`
- Type annotations required for TypeScript files

**Return Values:**
- React components return JSX elements
- Service functions return Promises or void (with callbacks)
- Utility functions return typed values
- Consistent return patterns within function type

**Null/Undefined Handling:**
```typescript
// Prefer null for initial state
const [error, setError] = React.useState(null);
const [selectedFilter, setSelectedFilter] = React.useState(null);

// Use optional chaining for nested properties
error?.response?.data
item?.firstName
props?.page?.pageNo
```

## Module Design

**Exports:**
- Default exports for main component/function - Example: `export default Users;`
- Named exports for utilities and constants
- Barrel files (index.tsx/index.ts) re-export from subdirectories

**Barrel File Pattern:**
```typescript
// index.tsx in component directory
import React from "react";
import UserManagement from "./users";
export default UserManagement;
```

**Component Composition:**
- Container components with data/state logic (`index.tsx`)
- Presentational components with rendering logic (e.g., `users.tsx`)
- Separation of concerns between logic and UI

## React Patterns

**Hooks:**
- `React.useState()` for state management
- `React.useEffect()` for side effects
- `React.memo()` for component memoization - Used on: `Users`, `UserManagement`
- `useTranslation()` from react-i18next for i18n
- `useHistory()` and `useParams()` from react-router-dom

**Props:**
- Props typed via interfaces when using TypeScript
- Props marked as `any` in some cases (legacy pattern)
- Spread syntax for passing multiple props: `<Component {...props} />`

**Rendering:**
- Conditional rendering with ternary operators: `condition ? <Component /> : <FallbackComponent />`
- Array mapping for lists: `items.map((item, i) => <Component key={i} {...item} />)`
- Fragment usage for multiple elements without wrapper

## State Management

**Pattern:** React local state (useState) + props drilling
- No Redux or Context API observed
- State managed at component level or container parent
- State passed down through props to child components

**Invalidation Pattern:**
```typescript
const [invalidated, setInvalidated] = React.useState(false);
React.useEffect(() => {
  if (invalidated) {
    // Re-fetch data
    setInvalidated(false);
  }
}, [invalidated]);
```

---

*Convention analysis: 2026-02-03*
