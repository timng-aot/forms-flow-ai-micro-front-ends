# Testing Patterns

**Analysis Date:** 2026-02-03

## Test Framework

**Runner:**
- Jest v27.0.6
- Config: `jest.config.js` in each package root
- Environment: jsdom (browser-like environment)

**Assertion Library:**
- Testing Library (`@testing-library/react` v12.0.0)
- Jest assertions (built-in)
- `@testing-library/jest-dom` v5.14.1 for DOM matchers

**Run Commands:**
```bash
npm run test                # Run all tests once
npm run watch-tests         # Run tests in watch mode
npm run coverage            # Run tests with coverage report
```

## Test File Organization

**Location:**
- Primary: Co-located in `__test__` directories - `src/__test__/` pattern
- Naming: `ComponentName.test.tsx`
- Structure exists per package (forms-flow-admin, forms-flow-components, etc.)

**Examples:**
- `forms-flow-components/src/__test__/button.test.tsx`
- `forms-flow-components/src/__test__/errorModal.test.tsx`
- `forms-flow-components/src/__test__/MultiSelect.test.tsx`
- `forms-flow-admin/src/root.component.test.tsx`

**Directory Pattern:**
```
src/
├── components/
│   └── CustomComponents/
│       ├── Button.tsx
│       └── ...
├── __test__/
│   ├── button.test.tsx
│   ├── errorModal.test.tsx
│   └── ...
└── ...
```

## Test Structure

**Suite Organization:**
```typescript
import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import "@testing-library/jest-dom";
import { ComponentName } from "../components/path/ComponentName";

describe("ComponentName Component", () => {
  it("renders component with expected content", () => {
    const { getByText } = render(<ComponentName />);
    expect(getByText("Text")).toBeInTheDocument();
  });

  it("handles user interactions", () => {
    const handleClick = jest.fn();
    const { getByRole } = render(<ComponentName onClick={handleClick} />);
    fireEvent.click(getByRole("button"));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

**Patterns:**
- `describe()` for test suites (one per component)
- `it()` for individual test cases
- `beforeEach()` for setup before each test
- `jest.clearAllMocks()` for clearing mock state between tests

**Setup Pattern:**
```typescript
describe('ComponentName', () => {
  const mockCallback = jest.fn();
  const mockOptions = [
    { id: '1', name: 'Option 1' },
    { id: '2', name: 'Option 2' }
  ];

  beforeEach(() => {
    jest.clearAllMocks();
  });

  // Tests...
});
```

## Mocking

**Framework:** Jest mocking (`jest.fn()`, `jest.mock()`)

**Patterns:**

**1. Mock Functions:**
```typescript
const mockOnClose = jest.fn();
const mockPrimaryAction = jest.fn();

// Usage in component
fireEvent.click(button);
expect(mockPrimaryAction).toHaveBeenCalled();
expect(mockPrimaryAction).toHaveBeenCalledTimes(1);
```

**2. Module Mocking (Setup):**
Location: `jest.setup.js` in forms-flow-components
```typescript
import "@testing-library/jest-dom";

// Mock `react-i18next` to avoid repetitive mocking
jest.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key) => key, // Mock translation function returns key as-is
  }),
}));
```

**3. Custom Module Mocks:**
Location: `__mocks__/@formsflow/service.js`
```typescript
export const HelperServices = {
  "getLocalDateAndTime": () => {}
};

export const StyleServices = {
  "getCSSVariable": (variableName) => {
    if (typeof globalThis.window !== 'undefined' && typeof document !== 'undefined') {
      return getComputedStyle(document.documentElement)
        .getPropertyValue(variableName)
        .trim();
    }
    return '';
  },
};

export const StorageService = {
  get: (key) => null,
  save: (key, value) => {},
  User: {
    USER_ROLE: 'UserRoles',
    USER_DETAILS: 'UserDetails',
  }
};
```

**Module Name Mapping:**
In `jest.config.js`:
```javascript
moduleNameMapper: {
  "\\.(css)$": "identity-obj-proxy",
  "single-spa-react/parcel": "single-spa-react/lib/cjs/parcel.cjs",
  "@formsflow/service": "<rootDir>/__mocks__/@formsflow/service.js"
}
```

**What to Mock:**
- External dependencies (react-i18next, services)
- API calls and HTTP requests
- Window/document APIs for specific tests
- CSS imports (mapped to identity-obj-proxy)

**What NOT to Mock:**
- React components being tested
- React hooks (unless testing hook behavior)
- Internal state management
- User interactions

## Fixtures and Factories

**Test Data Pattern:**
```typescript
const mockOptions = [
  { id: '1', name: 'Option 1' },
  { id: '2', name: 'Option 2' },
  { id: '3', name: 'Option 3' }
];

const defaultProps = {
  showBuildForm: true,
  onClose: mockOnClose,
  primaryBtnAction: mockPrimaryAction,
  nameError: "",
  description: "",
  modalHeader: "Create Form",
};

const renderFormBuilderModal = (props) =>
  render(<FormBuilderModal {...defaultProps, ...props} />);
```

**Location:**
- Inline in test file for simple data
- No separate fixtures directory observed
- Default props objects created at suite level

**Factories:**
- Render helper functions: `renderFormBuilderModal(props)`, `renderMultipleSelect(props)`
- Simplifies re-rendering with different props
- Centralizes render configuration

## Coverage

**Requirements:** No explicit coverage target enforced

**View Coverage:**
```bash
npm run coverage
```

**Configuration:**
- Coverage reports generated but not required to pass
- Coverage thresholds not specified in jest.config.js

## Test Types

**Unit Tests:**
- Scope: Single component or function
- Approach: Render component, test props, event handlers, conditional rendering
- Example: Button click handling, input value changes

**Integration Tests:**
- Limited use; primarily component-level
- Test component with child components
- Example: Modal with form inputs and buttons

**E2E Tests:**
- Not used in this codebase
- No Cypress, Playwright, or similar framework observed

## Common Patterns

**Component Rendering:**
```typescript
it("renders basic button with label", () => {
  const { getByText } = render(
    <CustomButton variant="primary" label="Test Button" />
  );
  expect(getByText("Test Button")).toBeInTheDocument();
});
```

**Event Testing:**
```typescript
it("handles click events", () => {
  const handleClick = jest.fn();
  const { getByText } = render(
    <CustomButton label="Click Me" onClick={handleClick} />
  );
  fireEvent.click(getByText("Click Me"));
  expect(handleClick).toHaveBeenCalledTimes(1);
});
```

**Form Input Testing:**
```typescript
it("updates name field on change", () => {
  const mockHandleChange = jest.fn();
  const { getByTestId } = render(
    <FormBuilderModal handleChange={mockHandleChange} {...defaultProps} />
  );
  const nameInput = getByTestId("form-name");
  fireEvent.change(nameInput, { target: { value: "New Form" } });
  expect(mockHandleChange).toHaveBeenCalledWith("title", expect.any(Object));
});
```

**Conditional Rendering:**
```typescript
it("renders disabled button", () => {
  const { getByRole } = render(
    <CustomButton variant="primary" label="Disabled" disabled={true} />
  );
  expect(getByRole("button")).toBeDisabled();
});
```

**State Updates:**
```typescript
it("displays selected options", () => {
  const selectedValues = [mockOptions[0], mockOptions[1]];
  const { container } = renderMultipleSelect({
    options: mockOptions,
    value: selectedValues,
    onChange: mockOnChange,
    placeholder: "Select options"
  });
  expect(screen.getByText('Option 1')).toBeInTheDocument();
  expect(screen.getByText('Option 2')).toBeInTheDocument();
});
```

**DOM Query Methods (in order of preference):**
- `getByTestId()` - for explicitly marked test elements
- `getByText()` - for text content
- `getByRole()` - for semantic roles
- `getByPlaceholderText()` - for input placeholders
- `container.querySelector()` - as fallback for complex queries

**Async Testing:**
```typescript
// Using beforeEach for async setup
beforeEach(() => {
  jest.clearAllMocks();
  // Async setup if needed
});
```

**Error/Failure Testing:**
```typescript
it("click primary button without value", () => {
  renderFormBuilderModal(defaultProps);
  fireEvent.click(screen.getByTestId("confirm-button"));
  expect(mockPrimaryAction).not.toHaveBeenCalled();
});
```

## Test Data Attributes

**Convention:** Use `data-testid` for test identification

**Pattern:**
```typescript
// Component
<Button data-testid="add-role-button">Add Role</Button>

// Test
fireEvent.click(screen.getByTestId("add-role-button"));
```

**Naming:** Descriptive kebab-case
- `form-name`
- `confirm-button`
- `users-add-role-button`
- `error-modal`
- `admin-users-table`

## Jest Configuration Details

**babel-jest transformer:**
```javascript
module.exports = {
  rootDir: "src",
  testEnvironment: "jsdom",
  transform: {
    "^.+\\.(j|t)sx?$": "babel-jest",
  },
  moduleNameMapper: {
    "\\.(css)$": "identity-obj-proxy",
    "single-spa-react/parcel": "single-spa-react/lib/cjs/parcel.cjs",
  },
  setupFilesAfterEnv: ["@testing-library/jest-dom"],
};
```

**Transform:** Uses Babel (configured via babel.config.json) for JavaScript/TypeScript
**Root:** Tests run from src/ directory
**Setup:** jest-dom matchers auto-loaded for all tests

---

*Testing analysis: 2026-02-03*
