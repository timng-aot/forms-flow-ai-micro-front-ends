# Forms-Flow Theme Audit
**Date:** 2026-02-04
**Source:** forms-flow-theme/scss
**Total SCSS Variables:** 465
**Total CSS Custom Properties:** 137
**Total SCSS Maps:** 9

## Summary Statistics

| Category | SCSS Variables | CSS Custom Properties | Total |
|----------|---------------|----------------------|-------|
| Borderradius | 23 | 9 | 32 |
| Color | 174 | 76 | 250 |
| Other | 38 | 3 | 41 |
| Shadow | 4 | 0 | 4 |
| Spacing | 157 | 30 | 187 |
| Transition | 25 | 0 | 25 |
| Typography | 44 | 19 | 63 |
| **Total** | **465** | **137** | **602** |

## Borderradius

### SCSS Variables

| Variable | Value | Computed | Source File | Usages |
|----------|-------|----------|-------------|--------|
| `$alert-border-radius` | `0.313rem` | `0.313rem` | scss/v8-scss/_alert.scss | 0 |
| `$border-radius` | `var(--border-radius)` | `N/A` | scss/v8-scss/_modal.scss | 0 |
| `$borderRadius` | `var(--border-radius)` | `N/A` | scss/v8-scss/_formEditActions.scss | 0 |
| `$borderRadiusModal` | `$base*1.5` | `$base*1.5` | scss/_theme.scss | 0 |
| `$btn-border-radius` | `50%` | `50%` | scss/_button.scss | 0 |
| `$button-border-radius` | `1.5625rem` | `1.5625rem` | scss/v8-scss/_button.scss | 0 |
| `$checkbox-border-radius` | `0.25rem` | `0.25rem` | scss/v8-scss/_checkbox.scss | 0 |
| `$checkbox-border-radius-small` | `0.1875rem` | `0.1875rem` | scss/v8-scss/_checkbox.scss | 0 |
| `$dropdown-border-radius` | `0.3125rem` | `0.3125rem` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-item-radius` | `0.313rem` | `0.313rem` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$dropdown-menu-radius` | `0.3125rem` | `0.3125rem` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$drp-calendar-radius` | `0.375rem` | `0.375rem` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-container-radius` | `.3125rem` | `.3125rem` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$form-builder-border-radius` | `4px` | `4px` | scss/v8-scss/_formbuilder.scss | 0 |
| `$form-builder-border-radius-round` | `50%` | `50%` | scss/v8-scss/_formbuilder.scss | 0 |
| `$form-input-border-radius` | `var(--radius-lg)` | `N/A` | scss/inputBox.scss | 0 |
| `$multiselect-border-radius` | `5px` | `5px` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-chip-border-radius` | `25px` | `25px` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$radius-lg` | `var(--radius-lg)` | `N/A` | scss/fileUpload.scss | 0 |
| `$search-input-border-radius` | `0.3125rem` | `0.3125rem` | scss/v8-scss/_search.scss | 0 |
| `$status-radius` | `50%` | `50%` | scss/_table.scss | 0 |
| `$switch-border-radius` | `0.75rem` | `0.75rem` | scss/v8-scss/_switch.scss | 0 |
| `$url-input-border-radius` | `0.3125rem` | `0.3125rem` | scss/v8-scss/_urlInput.scss | 0 |

### CSS Custom Properties

| Property | Value | Root Block | Source File | Usages |
|----------|-------|------------|-------------|--------|
| `--border-radius` | `0.3125rem` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--ff-border-radius` | `var(--border-radius) !important` | v8-theme | scss/v8-scss/_formbuilder.scss | 0 |
| `--lg-btn-border-radius` | `var(--radius-lg)` | theme | scss/_theme.scss | 0 |
| `--md-btn-border-radius` | `var(--radius-md)` | theme | scss/_theme.scss | 0 |
| `--radius-lg` | `1.59375rem` | theme | scss/_theme.scss | 0 |
| `--radius-md` | `1.34375rem` | theme | scss/_theme.scss | 0 |
| `--radius-modal` | `1.5rem` | theme | scss/_theme.scss | 0 |
| `--radius-sm` | `1.09375rem` | theme | scss/_theme.scss | 0 |
| `--sm-btn-border-radius` | `var(--radius-md)` | theme | scss/_theme.scss | 0 |

## Color

### SCSS Variables

| Variable | Value | Computed | Source File | Usages |
|----------|-------|----------|-------------|--------|
| `$Gray-darkest` | `var(--gray-darkest)` | `N/A` | scss/v8-scss/_tabs.scss | 0 |
| `$Gray-x-light` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_tabs.scss | 0 |
| `$Secondary` | `var(--secondary)` | `N/A` | scss/v8-scss/_tabs.scss | 0 |
| `$White-200` | `var(--white-200)` | `N/A` | scss/v8-scss/_tabs.scss | 0 |
| `$White-300` | `var(--white-300)` | `N/A` | scss/v8-scss/_tabs.scss | 0 |
| `$alert-shadow-error` | `0 0.125rem 0.5rem rgba(255, 87, 34, 0.1)` | `0 0.125rem 0.5rem rgba(255, 87, 34, 0.1)` | scss/v8-scss/_alert.scss | 0 |
| `$alert-shadow-focus` | `0 0.125rem 0.5rem rgba(137, 105, 242, 0.1)` | `0 0.125rem 0.5rem rgba(137, 105, 242, 0.1)` | scss/v8-scss/_alert.scss | 0 |
| `$alert-shadow-warning` | `0 0.125rem 0.5rem rgba(255, 152, 0, 0.1)` | `0 0.125rem 0.5rem rgba(255, 152, 0, 0.1)` | scss/v8-scss/_alert.scss | 0 |
| `$black` | `#000000` | `#000000` | scss/_theme.scss | 19 |
| `$black-color` | `var(--gray-darkest)` | `N/A` | scss/v8-scss/_modal.scss | 0 |
| `$box-shadow` | `0 10px 25px rgba(0, 0, 0, 0.15)` | `0 10px 25px rgba(0, 0, 0, 0.15)` | scss/v8-scss/_mixins.scss | 0 |
| `$btn-color` | `$black` | `#000000` | scss/_theme.scss | 0 |
| `$button-shadow-error` | `0 0.125rem 0.5rem rgba(255, 87, 34, 0.1)` | `0 0.125rem 0.5rem rgba(255, 87, 34, 0.1)` | scss/v8-scss/_button.scss | 0 |
| `$button-shadow-primary` | `0 0.125rem 0.5rem rgba(137, 105, 242, 0.15)` | `0 0.125rem 0.5rem rgba(137, 105, 242, 0.15)` | scss/v8-scss/_button.scss | 0 |
| `$button-shadow-secondary` | `0 0.125rem 0.25rem rgba(0, 0, 0, 0.1)` | `0 0.125rem 0.25rem rgba(0, 0, 0, 0.1)` | scss/v8-scss/_button.scss | 0 |
| `$button-shadow-warning` | `0 0.125rem 0.5rem rgba(255, 152, 0, 0.1)` | `0 0.125rem 0.5rem rgba(255, 152, 0, 0.1)` | scss/v8-scss/_button.scss | 0 |
| `$chevron-bg` | `#5e61f2` | `#5e61f2` | scss/collapsibleSidebar.scss | 0 |
| `$color-alert-bg` | `var(--white-200)` | `N/A` | scss/v8-scss/_alert.scss | 0 |
| `$color-alert-border` | `var(--gray-medium-dark)` | `N/A` | scss/v8-scss/_alert.scss | 0 |
| `$color-alert-error` | `var(--orange-100)` | `N/A` | scss/v8-scss/_alert.scss | 0 |
| `$color-alert-focus` | `var(--primary-dark)` | `N/A` | scss/v8-scss/_alert.scss | 0 |
| `$color-alert-passive` | `var(--gray-medium-dark)` | `N/A` | scss/v8-scss/_alert.scss | 0 |
| `$color-alert-text` | `var(--secondary-dark)` | `N/A` | scss/v8-scss/_alert.scss | 0 |
| `$color-alert-warning` | `var(--red-100)` | `N/A` | scss/v8-scss/_alert.scss | 0 |
| `$color-border` | `var(--secondary)` | `N/A` | scss/v8-scss/_search.scss | 0 |
| `$color-border-light` | `#ededed` | `#ededed` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$color-copy-button-bg` | `transparent` | `transparent` | scss/v8-scss/_urlInput.scss | 0 |
| `$color-copy-button-border` | `var(--gray-darkest)` | `N/A` | scss/v8-scss/_urlInput.scss | 0 |
| `$color-copy-button-hover-bg` | `transparent` | `transparent` | scss/v8-scss/_urlInput.scss | 0 |
| `$color-dark-gray` | `var(--gray-darkest)` | `N/A` | scss/v8-scss/_filterableDropdown.scss | 0 |
| `$color-darker-gray` | `var(--secondary-dark)` | `N/A` | scss/v8-scss/_filterableDropdown.scss | 0 |
| `$color-default-text` | `var(--secondary-dark)` | `N/A` | scss/v8-scss/_breadCrumbs.scss | 0 |
| `$color-disabled-gray` | `var(--gray-medium)` | `N/A` | scss/v8-scss/_search.scss | 0 |
| `$color-error` | `var(--orange-100)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$color-error-border` | `var(--orange-100)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$color-error-disabled` | `var(--gray-medium)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$color-error-light` | `var(--orange-100)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$color-error-selected` | `var(--orange-100)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$color-hover-bg` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_filterableDropdown.scss | 0 |
| `$color-light-gray` | `var(--white-200)` | `N/A` | scss/v8-scss/_filterableDropdown.scss | 0 |
| `$color-medium-gray` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_filterableDropdown.scss | 0 |
| `$color-minimized-text` | `var(--gray-medium-dark)` | `N/A` | scss/v8-scss/_breadCrumbs.scss | 0 |
| `$color-placeholder` | `var(--gray-medium-dark)` | `N/A` | scss/v8-scss/_search.scss | 0 |
| `$color-placeholder-disabled` | `var(--secondary)` | `N/A` | scss/v8-scss/_search.scss | 0 |
| `$color-placeholder-gray` | `var(--gray-dark)` | `N/A` | scss/v8-scss/_filterableDropdown.scss | 0 |
| `$color-primary` | `var(--vivid-100)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$color-primary-active` | `var(--primary)` | `N/A` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$color-primary-border` | `var(--primary-dark)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$color-primary-disabled` | `var(--gray-medium)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$color-primary-light` | `var(--primary-dark)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$color-primary-lighter` | `var(--primary-lighter)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$color-primary-selected` | `var(--primary)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$color-secondary-active` | `var(--secondary)` | `N/A` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$color-secondary-border` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$color-secondary-hover` | `var(--gray-darkest)` | `N/A` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$color-selected-bg` | `var(--primary)` | `N/A` | scss/v8-scss/_filterableDropdown.scss | 0 |
| `$color-selected-gray` | `var(--secondary)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$color-switch-bg-default` | `var(--gray-medium)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$color-switch-bg-disabled` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$color-switch-bg-off` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$color-switch-bg-off-binary` | `var(--red-100)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$color-switch-bg-on` | `var(--green-100)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$color-switch-bg-on-primary` | `var(--primary-dark)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$color-switch-border-disabled` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$color-switch-hover-gray` | `var(--gray-medium)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$color-switch-hover-green` | `var(--green-200)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$color-switch-hover-primary` | `var(--vivid-100)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$color-switch-hover-red` | `var(--red-200)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$color-switch-slider` | `var(--white-300)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$color-text-light` | `#b7b7b8` | `#b7b7b8` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$color-text-muted` | `#999` | `#999` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$color-text-placeholder` | `#b7b7b8` | `#b7b7b8` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$color-text-primary` | `#212529` | `#212529` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$color-text-secondary` | `#222` | `#222` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$color-url-input-bg` | `var(--white-200)` | `N/A` | scss/v8-scss/_urlInput.scss | 0 |
| `$color-url-input-border` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_urlInput.scss | 0 |
| `$color-url-input-border-focus` | `var(--gray-medium)` | `N/A` | scss/v8-scss/_urlInput.scss | 0 |
| `$color-url-input-fixed-text` | `var(--gray-darkest)` | `N/A` | scss/v8-scss/_urlInput.scss | 0 |
| `$color-url-input-message` | `var(--gray-darkest)` | `N/A` | scss/v8-scss/_urlInput.scss | 0 |
| `$color-url-input-text` | `var(--gray-darkest)` | `N/A` | scss/v8-scss/_urlInput.scss | 0 |
| `$color-warning` | `var(--red-100)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$color-warning-border` | `var(--red-100)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$color-warning-disabled` | `var(--gray-medium)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$color-warning-light` | `var(--red-100)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$color-warning-selected` | `var(--red-100)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$color-white` | `var(--white-300)` | `N/A` | scss/v8-scss/_search.scss | 0 |
| `$colorDivider` | `$gray-medium` | `#E4E6E7` | scss/_theme.scss | 0 |
| `$colorDividerDark` | `$gray-medium-dark` | `#AFB4B6` | scss/_theme.scss | 0 |
| `$colorMain` | `$gray-darkest` | `$gray-darkest` | scss/historyModal.scss | 0 |
| `$colorSecondary` | `$gray-medium` | `N/A` | scss/historyModal.scss | 0 |
| `$danger` | `var(--default-danger-color)` | `N/A` | scss/_theme.scss | 0 |
| `$danger-color` | `var(--ff-danger)` | `N/A` | scss/_aiAssistant.scss | 0 |
| `$default-font-color` | `var(--default-font-color)` | `N/A` | scss/fileUpload.scss | 0 |
| `$dropdown-primary-border` | `rgba(184, 171, 255, 0.5)` | `rgba(184, 171, 255, 0.5)` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-primary-border-hover` | `var(--primary-dark)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-primary-disabled-border` | `rgba(184, 171, 255, 0.25)` | `rgba(184, 171, 255, 0.25)` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-primary-selected-bg` | `var(--primary)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-secondary-border` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-secondary-border-hover` | `var(--gray-dark)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-secondary-hover-border` | `rgba(107, 114, 128, 0.3)` | `rgba(107, 114, 128, 0.3)` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-secondary-selected-bg` | `var(--secondary)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-shadow` | `0 0.25rem 0.25rem rgba(0, 0, 0, 0.25)` | `0 0.25rem 0.25rem rgba(0, 0, 0, 0.25)` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$drp-shadow-calendar` | `0 0.5rem 1rem rgba(0, 0, 0, 0.15)` | `0 0.5rem 1rem rgba(0, 0, 0, 0.15)` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-shadow-container` | `0 0.0625rem 0.125rem rgba(0, 0, 0, 0.03)` | `0 0.0625rem 0.125rem rgba(0, 0, 0, 0.03)` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$ff-black` | `var(--ff-black)` | `N/A` | scss/fileUpload.scss | 0 |
| `$ff-white` | `var(--ff-white)` | `N/A` | scss/fileUpload.scss | 0 |
| `$font-color` | `var(--secondary-dark)` | `N/A` | scss/v8-scss/_mixins.scss | 0 |
| `$form-builder-color-bg-black` | `black` | `black` | scss/v8-scss/_formbuilder.scss | 0 |
| `$form-builder-color-bg-transparent` | `transparent` | `transparent` | scss/v8-scss/_formbuilder.scss | 0 |
| `$form-builder-color-text` | `#535353` | `#535353` | scss/v8-scss/_formbuilder.scss | 0 |
| `$form-builder-shadow-color` | `rgb(182 182 182 / 20%)` | `rgb(182 182 182 / 20%)` | scss/v8-scss/_formbuilder.scss | 0 |
| `$gray-dark` | `var(--ff-gray-dark)` | `N/A` | scss/external/formio.scss | 0 |
| `$gray-darker` | `#424243` | `#424243` | scss/v8-scss/_breadCrumbs.scss | 0 |
| `$gray-darkest` | `var(--ff-gray-darkest)` | `N/A` | scss/external/formio.scss | 51 |
| `$gray-light` | `var(--gray-light)` | `N/A` | scss/v8-scss/_modal.scss | 0 |
| `$gray-medium` | `var(--gray-medium)` | `N/A` | scss/v8-scss/_modal.scss | 128 |
| `$gray-medium-dark` | `var(--gray-medium-dark)` | `N/A` | scss/v8-scss/_modal.scss | 0 |
| `$gray-medium-dark-color` | `var(--gray-darkest)` | `N/A` | scss/v8-scss/_ReusableLargeModal.scss | 0 |
| `$gray-medium-darker` | `var(--gray-medium-darker)` | `N/A` | scss/v8-scss/_variableSelection.scss | 0 |
| `$gray-x-light` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_variableSelection.scss | 0 |
| `$green` | `#57C20A` | `#57C20A` | scss/_theme.scss | 0 |
| `$green-color` | `var(--ff-green)` | `N/A` | scss/_table.scss | 0 |
| `$green-dark` | `#006621` | `#006621` | scss/_theme.scss | 0 |
| `$headerTextColor` | `var(--gray-dark)` | `N/A` | scss/v8-scss/_formEditActions.scss | 0 |
| `$input-error-box-shadow` | `0 0 0 0.2rem rgba(255, 0, 0, 0.25)` | `0 0 0 0.2rem rgba(255, 0, 0, 0.25)` | scss/inputBox.scss | 0 |
| `$multiselect-bg-color` | `var(--white-200)` | `N/A` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-border-color` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-disabled-color` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-label-color` | `var(--gray-dark)` | `N/A` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-primary-border` | `rgba(184, 171, 255, 0.5)` | `rgba(184, 171, 255, 0.5)` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-primary-border-disabled` | `rgba(184, 171, 255, 0.25)` | `rgba(184, 171, 255, 0.25)` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-primary-border-hover` | `var(--primary-dark)` | `N/A` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-secondary-border-hover` | `var(--gray-dark)` | `N/A` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-secondary-hover-border` | `rgba(107, 114, 128, 0.3)` | `rgba(107, 114, 128, 0.3)` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-shadow` | `0 4px 4px 0 rgba(0, 0, 0, 0.25)` | `0 4px 4px 0 rgba(0, 0, 0, 0.25)` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-text-color` | `var(--gray-darkest)` | `N/A` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-white-bg` | `var(--white-300)` | `N/A` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$no-code-secondary` | `#EA9389` | `#EA9389` | scss/_theme.scss | 0 |
| `$no-code-success` | `#1B9C85` | `#1B9C85` | scss/_theme.scss | 0 |
| `$no-code-warning` | `#faad14` | `#faad14` | scss/_theme.scss | 0 |
| `$pill-bg-color` | `var(--pill-bg-color)` | `N/A` | scss/_forms.scss | 0 |
| `$primary` | `var(--ff-primary)` | `N/A` | scss/external/formio.scss | 216 |
| `$primary-color` | `var(--ff-primary)` | `N/A` | scss/customDateRangePicker.scss | 0 |
| `$primary-light` | `var(--ff-primary-light)` | `N/A` | scss/external/formio.scss | 0 |
| `$primary-light-color` | `var(--ff-primary-light)` | `N/A` | scss/customDateRangePicker.scss | 0 |
| `$secondary` | `var(--secondary)` | `N/A` | scss/fileUpload.scss | 0 |
| `$secondary-dark` | `var(--secondary-dark)` | `N/A` | scss/v8-scss/_variableSelection.scss | 0 |
| `$secondary-dark-color` | `var(--secondary-dark)` | `N/A` | scss/v8-scss/_formCreateLayout.scss | 0 |
| `$select-custom-value-border-color` | `#E5E5E5` | `#E5E5E5` | scss/v8-scss/_selectWithCustomValue.scss | 0 |
| `$select-custom-value-placeholder-color` | `#999` | `#999` | scss/v8-scss/_selectWithCustomValue.scss | 0 |
| `$success` | `$green-dark` | `#006621` | scss/_theme.scss | 0 |
| `$switch-shadow-default` | `0 0.0625rem 0.1875rem rgba(0, 0, 0, 0.2)` | `0 0.0625rem 0.1875rem rgba(0, 0, 0, 0.2)` | scss/v8-scss/_switch.scss | 0 |
| `$ta-color-bg` | `var(--white-200)` | `N/A` | scss/v8-scss/_textArea.scss | 0 |
| `$ta-color-border` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_textArea.scss | 0 |
| `$ta-color-border-focus` | `var(--gray-dark)` | `N/A` | scss/v8-scss/_textArea.scss | 0 |
| `$ta-color-border-hover` | `var(--secondary-dark)` | `N/A` | scss/v8-scss/_textArea.scss | 0 |
| `$ta-color-placeholder` | `var(--gray-xx-light)` | `N/A` | scss/v8-scss/_textArea.scss | 0 |
| `$ta-color-placeholder-disabled` | `var(--gray-xx-light)` | `N/A` | scss/v8-scss/_textArea.scss | 0 |
| `$ta-color-text` | `var(--gray-darkest)` | `N/A` | scss/v8-scss/_textArea.scss | 0 |
| `$table-border-color` | `#DAD9DA` | `#DAD9DA` | scss/v8-scss/_table.scss | 0 |
| `$table-shadow` | `rgba(0, 0, 0, 0.25)` | `rgba(0, 0, 0, 0.25)` | scss/v8-scss/_table.scss | 0 |
| `$theme-colors` | `map-merge($theme-colors, $custom-colors)` | `map-merge($theme-colors, $custom-colors)` | scss/_theme.scss | 0 |
| `$ti-color-bg` | `var(--white-200)` | `N/A` | scss/v8-scss/_textInput.scss | 0 |
| `$ti-color-border` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_textInput.scss | 0 |
| `$ti-color-border-focus` | `var(--gray-dark)` | `N/A` | scss/v8-scss/_textInput.scss | 0 |
| `$ti-color-border-hover` | `var(--secondary-dark)` | `N/A` | scss/v8-scss/_textInput.scss | 0 |
| `$ti-color-placeholder` | `var(--gray-dark)` | `N/A` | scss/v8-scss/_textInput.scss | 0 |
| `$ti-color-placeholder-disabled` | `var(--gray-xx-light)` | `N/A` | scss/v8-scss/_textInput.scss | 0 |
| `$ti-color-text` | `var(--gray-darkest)` | `N/A` | scss/v8-scss/_textInput.scss | 0 |
| `$transparent` | `#f2f2f300` | `#f2f2f300` | scss/_theme.scss | 0 |
| `$white` | `#fff` | `#fff` | scss/v8-scss/_theme.scss | 127 |
| `$white-100-color` | `var(--white-100)` | `N/A` | scss/v8-scss/_formCreateLayout.scss | 0 |
| `$white-200` | `var(--white-200)` | `N/A` | scss/v8-scss/_filterDropdown.scss | 0 |
| `$white-color` | `var(--ff-white)` | `N/A` | scss/collapsibleSidebar.scss | 0 |

### CSS Custom Properties

| Property | Value | Root Block | Source File | Usages |
|----------|-------|------------|-------------|--------|
| `--blue-100` | `blend-with-white-to-hex(#0087D9, 1.0)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--blue-200` | `blend-with-white-to-hex(#0087D9, 0.5)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--blue-300` | `blend-with-white-to-hex(#0087D9, 0.25)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--cyan-100` | `blend-with-white-to-hex(#00BCD4, 1.0)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--cyan-200` | `blend-with-white-to-hex(#00BCD4, 0.5)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--cyan-300` | `blend-with-white-to-hex(#00BCD4, 0.25)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--default-danger-color` | `#FF4242` | theme | scss/_theme.scss | 0 |
| `--default-font-color` | `#{$gray-dark}` | theme | scss/_theme.scss | 0 |
| `--default-link-color` | `#{$primary}` | theme | scss/_theme.scss | 0 |
| `--ff-link-color-rgb` | `var(--ff-primary) !important` | v8-theme | scss/v8-scss/_formbuilder.scss | 0 |
| `--ff-nav-link-color` | `var(--secondary-dark) !important` | v8-theme | scss/v8-scss/_formbuilder.scss | 0 |
| `--ff-nav-link-hover-color` | `var(--gray-darkest) !important` | v8-theme | scss/v8-scss/_formbuilder.scss | 0 |
| `--ff-primary` | `var(--gray-darkest) !important` | v8-theme | scss/v8-scss/_formbuilder.scss | 0 |
| `--gray-dark` | `#7C7D7F` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--gray-darkest` | `#4A4A4A` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--gray-light` | `#D9D9D9` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--gray-medium` | `#D1D2D3` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--gray-medium-dark` | `#B7B7B8` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--gray-medium-darker` | `#9E9E9E` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--gray-x-light` | `#E5E5E5` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--gray-xx-light` | `#DAD9DA` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--green-100` | `blend-with-white-to-hex(#00C49A, 1.0)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--green-200` | `blend-with-white-to-hex(#00C49A, 0.5)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--green-300` | `blend-with-white-to-hex(#00C49A, 0.25)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--indigo-100` | `blend-with-white-to-hex(#3248F4, 1.0)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--indigo-200` | `blend-with-white-to-hex(#3248F4, 0.5)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--indigo-300` | `blend-with-white-to-hex(#3248F4, 0.25)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--nav-bg-color` | `var(--white-100)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--navbar-active-submenu-bg-color` | `#{$gray-darkest}` | theme | scss/_theme.scss | 0 |
| `--navbar-active-submenu-font-color` | `#{$white}` | theme | scss/_theme.scss | 0 |
| `--navbar-bg-color` | `#{$white}` | theme | scss/_theme.scss | 0 |
| `--navbar-hover-submenu-bg-color` | `#{$primary-light}` | theme | scss/_theme.scss | 0 |
| `--navbar-hover-submenu-font-color` | `#{$gray-darkest}` | theme | scss/_theme.scss | 0 |
| `--navbar-main-menu-active-bg-color` | `#{$gray-medium}` | theme | scss/_theme.scss | 0 |
| `--navbar-main-menu-active-font-color` | `#{$gray-darkest}` | theme | scss/_theme.scss | 0 |
| `--navbar-menu-font-color` | `var(--secondary-dark)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--navbar-menu-font-color-active` | `var(--vivid)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--navbar-menu-hover-bg-color` | `#{$primary-light}` | theme | scss/_theme.scss | 0 |
| `--navbar-submenu-font-color` | `var(--gray-dark)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--no-code-secondary` | `#{$no-code-secondary}` | theme | scss/_theme.scss | 0 |
| `--no-code-success` | `#{$no-code-success}` | theme | scss/_theme.scss | 0 |
| `--no-code-warning` | `#{$no-code-warning}` | theme | scss/_theme.scss | 0 |
| `--orange-100` | `blend-with-white-to-hex(#FF9100, 1.0)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--orange-200` | `blend-with-white-to-hex(#FF9100, 0.5)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--orange-300` | `blend-with-white-to-hex(#FF9100, 0.25)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--pill-bg-color` | `var(--gray-x-light)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--primary` | `#F1EEFF` | v8-theme | scss/v8-scss/_theme.scss | 63 |
| `--primary-btn-bg-color` | `#{$primary}` | theme | scss/_theme.scss | 0 |
| `--primary-btn-font-color` | `#{$white}` | theme | scss/_theme.scss | 0 |
| `--primary-dark` | `#B8ABFF` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--primary-font` | `var(--font-family-base)` | theme | scss/_theme.scss | 0 |
| `--progress-bar-bg-color` | `var(--primary-dark)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--red-100` | `blend-with-white-to-hex(#E57373, 1.0)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--red-200` | `blend-with-white-to-hex(#E57373, 0.5)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--red-300` | `blend-with-white-to-hex(#E57373, 0.25)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--secondary` | `#EDEDED` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--secondary-btn-bg-color` | `#{$primary-light}` | theme | scss/_theme.scss | 0 |
| `--secondary-btn-font-color` | `#{$primary}` | theme | scss/_theme.scss | 0 |
| `--secondary-dark` | `#525254` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--shadow-2xl` | `0px 20px 24px -4px rgba(48, 52, 54, 0.08)` | theme | scss/_theme.scss | 0 |
| `--shadow-3xl` | `0px 24px 48px -8px rgba(48, 52, 54, 0.016)` | theme | scss/_theme.scss | 0 |
| `--shadow-lg` | `0px 4px 8px -2px rgba(48, 52, 54, 0.08)` | theme | scss/_theme.scss | 0 |
| `--shadow-md` | `0px 2px 4px 0px rgba(48, 52, 54, 0.08)` | theme | scss/_theme.scss | 0 |
| `--shadow-nav` | `4px 0px 8px -2px rgba(48, 52, 54, 0.08)` | theme | scss/_theme.scss | 0 |
| `--shadow-sm` | `0px 2px 2px 0px rgba(48, 52, 54, 0.04)` | theme | scss/_theme.scss | 0 |
| `--shadow-xl` | `0px 12px 16px -4px rgba(48, 52, 54, 0.08)` | theme | scss/_theme.scss | 0 |
| `--vivid` | `#7C80FE` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--vivid-100` | `blend-with-white-to-hex(#7C80FE, 1.0)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--vivid-200` | `blend-with-white-to-hex(#7C80FE, 0.5)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--vivid-300` | `blend-with-white-to-hex(#7C80FE, 0.25)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--white-100` | `#F6F6F6` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--white-200` | `#FCFCFC` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--white-300` | `#FFFFFF` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--yellow-100` | `blend-with-white-to-hex(#EFC005, 1.0)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--yellow-200` | `blend-with-white-to-hex(#EFC005, 0.5)` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--yellow-300` | `blend-with-white-to-hex(#EFC005, 0.25)` | v8-theme | scss/v8-scss/_theme.scss | 0 |

## Other

### SCSS Variables

| Variable | Value | Computed | Source File | Usages |
|----------|-------|----------|-------------|--------|
| `$breadcrumb-divider` | `">"` | `">"` | scss/v8-scss/_breadCrumbs.scss | 0 |
| `$breadcrumb-underline-offset` | `0.1875rem` | `0.1875rem` | scss/v8-scss/_breadCrumbs.scss | 0 |
| `$button-focus-outline-offset` | `2px` | `2px` | scss/v8-scss/_button.scss | 0 |
| `$checkboxSize` | `calc($base + $paddingLvl5S*2)` | `calc($base + $paddingLvl5S*2)` | scss/_button.scss | 0 |
| `$deleteBorder` | `var(--red-200)` | `N/A` | scss/v8-scss/_formEditActions.scss | 0 |
| `$deleteHeader` | `var(--red-100)` | `N/A` | scss/v8-scss/_formEditActions.scss | 0 |
| `$dropdown-z-index` | `1000` | `1000` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$form-input-focus-outline` | `2px solid var(--ff-primary)` | `2px solid var(--ff-primary)` | scss/inputBox.scss | 0 |
| `$iconCloseSize` | `$base` | `1rem` | scss/_modal.scss | 0 |
| `$importBackground` | `var(--white-200)` | `N/A` | scss/v8-scss/_formEditActions.scss | 0 |
| `$lineThick` | `$lineThin*2` | `$lineThin*2` | scss/_theme.scss | 0 |
| `$lineThin` | `1px` | `1px` | scss/_theme.scss | 0 |
| `$multiselect-z-index` | `9999` | `9999` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$new-b` | `round((blue($color) * $opacity) + (blue($white) * ` | `round((blue($color) * $opacity) + (blue($white) * ` | scss/v8-scss/_theme.scss | 0 |
| `$new-g` | `round((green($color) * $opacity) + (green($white) ` | `round((green($color) * $opacity) + (green($white) ` | scss/v8-scss/_theme.scss | 0 |
| `$new-r` | `round((red($color) * $opacity) + (red($white) * (1` | `round((red($color) * $opacity) + (red($white) * (1` | scss/v8-scss/_theme.scss | 0 |
| `$prefix` | `"ff-"` | `"ff-"` | scss/_variables.scss | 0 |
| `$progressBorder` | `var(--gray-light)` | `N/A` | scss/v8-scss/_formEditActions.scss | 0 |
| `$resizerSize` | `$base` | `$base` | scss/_table.scss | 0 |
| `$sectionBackground` | `var(--white-200)` | `N/A` | scss/v8-scss/_formEditActions.scss | 0 |
| `$size` | `calc(20 * $base)` | `calc(20 * $base)` | scss/collapsibleSidebar.scss | 0 |
| `$sizeOfSlash` | `$base` | `$base` | scss/_button.scss | 0 |
| `$spaceBetween` | `var(--spacer-150)` | `N/A` | scss/_card.scss | 0 |
| `$spaceBetweenElementsInside` | `$paddingLvl5S` | `$paddingLvl5S` | scss/historyModal.scss | 0 |
| `$spaceBetweenElementsInsideBP1` | `$paddingLvl5TB` | `$paddingLvl5TB` | scss/historyModal.scss | 0 |
| `$spaceBetweenSubElements` | `var(--spacer-100)` | `N/A` | scss/_card.scss | 0 |
| `$spaceBetweenVersions` | `$paddingLvl5S` | `$paddingLvl5S` | scss/historyModal.scss | 0 |
| `$spacing` | `$paddingLvl4S` | `$paddingLvl4S` | scss/_button.scss | 0 |
| `$spacingAround` | `$base` | `1rem` | scss/_modal.scss | 0 |
| `$spacingBetween` | `$base/2` | `$base/2` | scss/_modal.scss | 0 |
| `$spacingBetweenLabels` | `$base/4` | `$base/4` | scss/_modal.scss | 0 |
| `$status-size` | `var(--spacer-050)` | `N/A` | scss/_table.scss | 0 |
| `$table-bg-light` | `var( --white-300)` | `N/A` | scss/v8-scss/_table.scss | 0 |
| `$table-border-light` | `var(--gray-x-light)` | `N/A` | scss/v8-scss/_table.scss | 0 |
| `$th-z-index-default` | `2` | `2` | scss/_table.scss | 0 |
| `$th-z-index-special` | `3` | `3` | scss/_table.scss | 0 |
| `$timelineLineLeft` | `$base*5` | `$base*5` | scss/historyModal.scss | 0 |
| `$url-input-placeholder` | `var(--gray-xx-light)` | `N/A` | scss/v8-scss/_urlInput.scss | 0 |

### CSS Custom Properties

| Property | Value | Root Block | Source File | Usages |
|----------|-------|------------|-------------|--------|
| `--custom-logo-path` | `" "` | theme | scss/_theme.scss | 0 |
| `--custom-title` | `" "` | theme | scss/_theme.scss | 0 |
| `--main-bg` | `var(--white-300)` | v8-theme | scss/v8-scss/_theme.scss | 0 |

## Shadow

### SCSS Variables

| Variable | Value | Computed | Source File | Usages |
|----------|-------|----------|-------------|--------|
| `$form-builder-shadow` | `$form-builder-shadow-color 0px 2px 8px 0px` | `$form-builder-shadow-color 0px 2px 8px 0px` | scss/v8-scss/_formbuilder.scss | 0 |
| `$switch-shadow-focus` | `0 0 0 1px` | `0 0 0 1px` | scss/v8-scss/_switch.scss | 0 |
| `$switch-shadow-hover` | `0 0 0 2px` | `0 0 0 2px` | scss/v8-scss/_switch.scss | 0 |
| `$url-input-shadow-focus` | `0 0 0 1px` | `0 0 0 1px` | scss/v8-scss/_urlInput.scss | 0 |

### CSS Custom Properties

| Property | Value | Root Block | Source File | Usages |
|----------|-------|------------|-------------|--------|
| - | - | - | - | - |

## Spacing

### SCSS Variables

| Variable | Value | Computed | Source File | Usages |
|----------|-------|----------|-------------|--------|
| `$BP1` | `47em` | `47em` | scss/_table.scss | 0 |
| `$alert-border-width` | `1px` | `1px` | scss/v8-scss/_alert.scss | 0 |
| `$alert-gap` | `var(--spacer-050)` | `N/A` | scss/v8-scss/_alert.scss | 0 |
| `$alert-line-height` | `var(--line-height-default)` | `N/A` | scss/v8-scss/_alert.scss | 0 |
| `$alert-min-height` | `3.5rem` | `3.5rem` | scss/v8-scss/_alert.scss | 0 |
| `$alert-padding` | `0 1.375rem` | `0 1.375rem` | scss/v8-scss/_alert.scss | 0 |
| `$alert-slide-distance` | `1rem` | `1rem` | scss/v8-scss/_alert.scss | 0 |
| `$base` | `1rem` | `1rem` | scss/v8-scss/_modal.scss | 97 |
| `$borderRadiusHeightESM` | `$base*0.78` | `$base*0.78` | scss/_theme.scss | 0 |
| `$borderRadiusHeightL` | `$base*1.594` | `$base*1.594` | scss/_theme.scss | 0 |
| `$borderRadiusHeightM` | `$base*1.344` | `$base*1.344` | scss/_theme.scss | 0 |
| `$borderRadiusHeightSM` | `$base*1.094` | `$base*1.094` | scss/_theme.scss | 0 |
| `$breadcrumb-gap` | `0.5rem` | `0.5rem` | scss/v8-scss/_breadCrumbs.scss | 0 |
| `$button-active-transform` | `1px` | `1px` | scss/v8-scss/_button.scss | 0 |
| `$button-border-width` | `1px` | `1px` | scss/v8-scss/_button.scss | 0 |
| `$button-focus-outline-width` | `2px` | `2px` | scss/v8-scss/_button.scss | 0 |
| `$button-gap` | `var(--spacer-050)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$button-icon-padding` | `0.75rem` | `0.75rem` | scss/v8-scss/_button.scss | 0 |
| `$button-line-height` | `var(--line-height-default)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$button-min-height` | `2.5rem` | `2.5rem` | scss/v8-scss/_button.scss | 0 |
| `$button-min-width` | `5rem` | `5rem` | scss/v8-scss/_button.scss | 0 |
| `$button-padding` | `0.6875rem 1.375rem` | `0.6875rem 1.375rem` | scss/v8-scss/_button.scss | 0 |
| `$checkbox-border-width` | `2px` | `2px` | scss/v8-scss/_checkbox.scss | 0 |
| `$checkbox-border-width-small` | `2px` | `2px` | scss/v8-scss/_checkbox.scss | 0 |
| `$checkbox-size` | `33px` | `33px` | scss/v8-scss/_checkbox.scss | 0 |
| `$checkbox-size-small` | `16px` | `16px` | scss/v8-scss/_checkbox.scss | 0 |
| `$checkmark-border-width` | `2px` | `2px` | scss/v8-scss/_checkbox.scss | 0 |
| `$checkmark-border-width-small` | `2px` | `2px` | scss/v8-scss/_checkbox.scss | 0 |
| `$checkmark-height` | `16px` | `16px` | scss/v8-scss/_checkbox.scss | 0 |
| `$checkmark-height-small` | `8px` | `8px` | scss/v8-scss/_checkbox.scss | 0 |
| `$checkmark-transform` | `translate(-50%, -70%) rotate(45deg) scale(1)` | `translate(-50%, -70%) rotate(45deg) scale(1)` | scss/v8-scss/_checkbox.scss | 0 |
| `$checkmark-width` | `9px` | `9px` | scss/v8-scss/_checkbox.scss | 0 |
| `$checkmark-width-small` | `5px` | `5px` | scss/v8-scss/_checkbox.scss | 0 |
| `$copy-button-icon-size` | `1.5rem` | `1.5rem` | scss/v8-scss/_urlInput.scss | 0 |
| `$copy-button-size` | `1.5rem` | `1.5rem` | scss/v8-scss/_urlInput.scss | 0 |
| `$detailsWidth` | `$base*8` | `$base*8` | scss/historyModal.scss | 0 |
| `$dropdown-border-width` | `0.0625rem` | `0.0625rem` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$dropdown-btn-size` | `3.2275rem` | `3.2275rem` | scss/_button.scss | 0 |
| `$dropdown-divider-width` | `0.0625rem` | `0.0625rem` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$dropdown-gap` | `var(--spacer-050)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-height` | `2.5rem` | `2.5rem` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-icon-padding` | `0.875rem 0.875rem 0.6875rem 0.8125rem` | `0.875rem 0.875rem 0.6875rem 0.8125rem` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$dropdown-item-padding` | `0.3125rem 0.5rem 0.5625rem 0.625rem` | `0.3125rem 0.5rem 0.5625rem 0.625rem` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$dropdown-label-padding` | `5px` | `5px` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$dropdown-line-height` | `var(--line-height-default)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-max-height` | `8.75rem` | `8.75rem` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-menu-padding` | `0.875rem 0.375rem` | `0.875rem 0.375rem` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$dropdown-padding` | `var(--spacer-050) var(--spacer-075)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-width` | `22rem` | `22rem` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdownMaxHeight` | `14rem` | `14rem` | scss/_button.scss | 0 |
| `$drp-calendar-margin-top` | `0.3125rem` | `0.3125rem` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-calendar-width` | `18.75rem` | `18.75rem` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-container-height` | `2.5rem` | `2.5rem` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-container-padding` | `0.25rem 0.75rem` | `0.25rem 0.75rem` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-container-width` | `18.75rem` | `18.75rem` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-input-padding` | `0.3125rem 0.375rem` | `0.3125rem 0.375rem` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-line-height` | `1.5` | `1.5` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-separator-margin` | `0 0.25rem` | `0 0.25rem` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$expanded-width` | `20rem` | `20rem` | scss/collapsibleSidebar.scss | 0 |
| `$font-family-base` | `var(--font-family-base)` | `N/A` | scss/v8-scss/_mixins.scss | 0 |
| `$font-weight-base` | `var(--font-weight-regular)` | `N/A` | scss/v8-scss/_breadCrumbs.scss | 0 |
| `$fontBase` | `$base` | `0.5rem` | scss/_theme.scss | 0 |
| `$fontLineHeight` | `1.2` | `1.2` | scss/_theme.scss | 0 |
| `$form-builder-border-width` | `1px` | `1px` | scss/v8-scss/_formbuilder.scss | 0 |
| `$form-builder-border-width-thick` | `2px` | `2px` | scss/v8-scss/_formbuilder.scss | 0 |
| `$form-builder-breakpoint` | `1550px` | `1550px` | scss/v8-scss/_formbuilder.scss | 0 |
| `$form-builder-gap` | `1rem` | `1rem` | scss/v8-scss/_formbuilder.scss | 0 |
| `$form-builder-spacing-lg` | `80px` | `80px` | scss/v8-scss/_formbuilder.scss | 0 |
| `$form-builder-spacing-md` | `16px` | `16px` | scss/v8-scss/_formbuilder.scss | 0 |
| `$form-builder-spacing-sm` | `5px` | `5px` | scss/v8-scss/_formbuilder.scss | 0 |
| `$height` | `776px` | `776px` | scss/v8-scss/_mixins.scss | 0 |
| `$iconWidth` | `$base` | `0.5rem` | scss/_theme.scss | 0 |
| `$leftSideWidth` | `25rem` | `25rem` | scss/_modal.scss | 0 |
| `$line-height-default` | `var(--line-height-default)` | `N/A` | scss/v8-scss/_mixins.scss | 0 |
| `$maxWidth` | `15rem` | `15rem` | scss/_button.scss | 0 |
| `$minHeight` | `calc($base*5)` | `calc($base*5)` | scss/_button.scss | 0 |
| `$minHeightLarge` | `calc($base*23)` | `calc($base*23)` | scss/_button.scss | 0 |
| `$modal-height` | `80vh` | `80vh` | scss/v8-scss/_mixins.scss | 0 |
| `$modal-width` | `40vw` | `40vw` | scss/v8-scss/_modal.scss | 0 |
| `$modal-width-max` | `550px` | `550px` | scss/v8-scss/_modal.scss | 0 |
| `$modal-width-min` | `400px` | `400px` | scss/v8-scss/_modal.scss | 0 |
| `$modalOutterPadding` | `$base` | `0.5rem` | scss/_theme.scss | 0 |
| `$modalWidthLarge` | `$base*75` | `$base*75` | scss/_theme.scss | 0 |
| `$modalWidthSmall` | `$base*60` | `$base*60` | scss/_theme.scss | 0 |
| `$multiselect-chip-padding` | `11px 18px 11px 16px` | `11px 18px 11px 16px` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-gap` | `var(--spacer-100)` | `N/A` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-margin-top` | `8px` | `8px` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-option-padding` | `8px` | `8px` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$multiselect-width` | `100%` | `100%` | scss/v8-scss/_dropdownMultiselect.scss | 0 |
| `$navPadding` | `$base` | `0.5rem` | scss/_theme.scss | 0 |
| `$override-font-base` | `1rem` | `1rem` | scss/_forms.scss | 0 |
| `$paddingLR` | `var(--spacer-200)` | `N/A` | scss/_card.scss | 0 |
| `$paddingLvl1LR` | `var(--spacer-300)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl1S` | `var(--spacer-200)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl1TB` | `var(--spacer-250)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl2LR` | `var(--spacer-250)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl2MinLR` | `var(--spacer-250)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl2MinS` | `var(--spacer-100)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl2MinTB` | `var(--spacer-100)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl2S` | `var(--spacer-150)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl2TB` | `var(--spacer-200)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl3LR` | `var(--spacer-150)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl3MinLR` | `var(--spacer-100)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl3MinS` | `var(--spacer-050)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl3MinTB` | `var(--spacer-050)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl3S` | `var(--spacer-100)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl3TB` | `var(--spacer-125)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl4LR` | `var(--spacer-125)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl4S` | `var(--spacer-050)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl4TB` | `var(--spacer-100)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl5LR` | `var(--spacer-100)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl5S` | `var(--spacer-050)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl5TB` | `var(--spacer-075)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl6LR` | `var(--spacer-075)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl6S` | `var(--spacer-025)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl6TB` | `var(--spacer-050)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl7LR` | `var(--spacer-025)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl7S` | `var(--spacer-025)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingLvl7TB` | `var(--spacer-050)` | `N/A` | scss/_mixins.scss | 0 |
| `$paddingRL` | `$base` | `1rem` | scss/_modal.scss | 0 |
| `$paddingTB` | `$base/2` | `$base/2` | scss/_modal.scss | 0 |
| `$radio-dot-size` | `0.625rem` | `0.625rem` | scss/v8-scss/_radio.scss | 0 |
| `$radio-gap-inline` | `2rem` | `2rem` | scss/v8-scss/_radio.scss | 0 |
| `$radio-ring-width` | `0.125rem` | `0.125rem` | scss/v8-scss/_radio.scss | 0 |
| `$radio-size` | `1.25rem` | `1.25rem` | scss/v8-scss/_radio.scss | 0 |
| `$rightSideWidth` | `20rem` | `20rem` | scss/_modal.scss | 0 |
| `$scrollBarWidth` | `0.5rem` | `0.5rem` | scss/v8-scss/_theme.scss | 0 |
| `$search-input-gap` | `var(--spacer-100)` | `N/A` | scss/v8-scss/_search.scss | 0 |
| `$search-input-height` | `2.5rem` | `2.5rem` | scss/v8-scss/_search.scss | 0 |
| `$search-input-padding` | `0.6875rem 0.8125rem` | `0.6875rem 0.8125rem` | scss/v8-scss/_search.scss | 0 |
| `$search-max-width` | `40rem` | `40rem` | scss/v8-scss/_search.scss | 0 |
| `$select-custom-value-max-height` | `14.75rem` | `14.75rem` | scss/v8-scss/_selectWithCustomValue.scss | 0 |
| `$select-custom-value-special-item-padding` | `24px` | `24px` | scss/v8-scss/_selectWithCustomValue.scss | 0 |
| `$sideElementWidth` | `calc($base*15)` | `calc($base*15)` | scss/_table.scss | 0 |
| `$spacer-050` | `var(--spacer-050)` | `N/A` | scss/fileUpload.scss | 0 |
| `$spacer-100` | `var(--spacer-100)` | `N/A` | scss/fileUpload.scss | 0 |
| `$spacer-150` | `var(--spacer-150)` | `N/A` | scss/fileUpload.scss | 0 |
| `$spacer-200` | `var(--spacer-200)` | `N/A` | scss/fileUpload.scss | 0 |
| `$spinner-border-width` | `0.125em` | `0.125em` | scss/v8-scss/_button.scss | 0 |
| `$spinner-size` | `1em` | `1em` | scss/v8-scss/_button.scss | 0 |
| `$status-margin` | `var(--spacer-050)` | `N/A` | scss/_table.scss | 0 |
| `$switch-border-width` | `1px` | `1px` | scss/v8-scss/_switch.scss | 0 |
| `$switch-gap` | `var(--spacer-050)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$switch-height` | `1.5rem` | `1.5rem` | scss/v8-scss/_switch.scss | 0 |
| `$switch-slider-offset` | `0.125rem` | `0.125rem` | scss/v8-scss/_switch.scss | 0 |
| `$switch-slider-size` | `1.25rem` | `1.25rem` | scss/v8-scss/_switch.scss | 0 |
| `$switch-slider-translate` | `1.375rem` | `1.375rem` | scss/v8-scss/_switch.scss | 0 |
| `$switch-width` | `2.75rem` | `2.75rem` | scss/v8-scss/_switch.scss | 0 |
| `$table-scrollbar-padding` | `1rem` | `1rem` | scss/_table.scss | 0 |
| `$text-line-height` | `120%` | `120%` | scss/fileUpload.scss | 0 |
| `$th-width` | `8.125rem` | `8.125rem` | scss/_table.scss | 0 |
| `$url-input-border-width` | `1px` | `1px` | scss/v8-scss/_urlInput.scss | 0 |
| `$url-input-focus-outline-width` | `1px` | `1px` | scss/v8-scss/_urlInput.scss | 0 |
| `$url-input-gap` | `0.5rem` | `0.5rem` | scss/v8-scss/_urlInput.scss | 0 |
| `$url-input-padding` | `1rem` | `1rem` | scss/v8-scss/_urlInput.scss | 0 |
| `$url-input-padding-desktop` | `2rem` | `2rem` | scss/v8-scss/_urlInput.scss | 0 |
| `$width` | `75vw` | `75vw` | scss/v8-scss/_mixins.scss | 0 |

### CSS Custom Properties

| Property | Value | Root Block | Source File | Usages |
|----------|-------|------------|-------------|--------|
| `--body-section-height` | `100vh` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--client-nav` | `74px` | theme | scss/_theme.scss | 0 |
| `--custom-logo-height` | `1.5rem` | theme | scss/_theme.scss | 0 |
| `--font-family-base` | `"Figtree", sans-serif` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--header-close-btn` | `4.625rem` | theme | scss/_theme.scss | 0 |
| `--letter-spacing-default` | `0%` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--line-height-default` | `100%` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--navbar-active-submenu-font-size` | `var(--font-size-sm)` | theme | scss/_theme.scss | 0 |
| `--navbar-active-submenu-font-weight` | `var(--font-weight-lg)` | theme | scss/_theme.scss | 0 |
| `--navbar-hover-submenu-font-size` | `var(--font-size-xs)` | theme | scss/_theme.scss | 0 |
| `--navbar-hover-submenu-font-weight` | `var(--font-weight-xl)` | theme | scss/_theme.scss | 0 |
| `--navbar-width` | `3rem` | v8-theme | scss/v8-scss/_theme.scss | 3 |
| `--spacer-025` | `0.25rem` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--spacer-050` | `0.5rem` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--spacer-075` | `0.75rem` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--spacer-100` | `1rem` | v8-theme | scss/v8-scss/_theme.scss | 62 |
| `--spacer-125` | `1.25rem` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--spacer-150` | `1.5rem` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--spacer-175` | `1.75rem` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--spacer-200` | `2rem` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--spacer-225` | `2.25rem` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--spacer-250` | `2.5rem` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--spacer-275` | `2.75rem` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--spacer-300` | `3rem` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--text-line-height` | `120%` | theme | scss/_theme.scss | 0 |
| `--text-space-lg` | `0.16rem` | theme | scss/_theme.scss | 0 |
| `--text-space-md` | `0.08rem` | theme | scss/_theme.scss | 0 |
| `--text-space-sm` | `0.04rem` | theme | scss/_theme.scss | 0 |
| `--text-space-xl` | `0.2rem` | theme | scss/_theme.scss | 0 |
| `--text-space-xs` | `0.02rem` | theme | scss/_theme.scss | 0 |

## Transition

### SCSS Variables

| Variable | Value | Computed | Source File | Usages |
|----------|-------|----------|-------------|--------|
| `$alert-enter-duration` | `0.3s` | `0.3s` | scss/v8-scss/_alert.scss | 0 |
| `$alert-exit-duration` | `0.2s` | `0.2s` | scss/v8-scss/_alert.scss | 0 |
| `$alert-transition-duration` | `0.3s` | `0.3s` | scss/v8-scss/_alert.scss | 0 |
| `$alert-transition-timing` | `ease-in-out` | `ease-in-out` | scss/v8-scss/_alert.scss | 0 |
| `$animSpeed` | `300ms` | `300ms` | scss/v8-scss/_dragandrop.scss | 0 |
| `$breadcrumb-transition-duration` | `0.15s` | `0.15s` | scss/v8-scss/_breadCrumbs.scss | 0 |
| `$breadcrumb-transition-timing` | `ease-in-out` | `ease-in-out` | scss/v8-scss/_breadCrumbs.scss | 0 |
| `$button-transition-duration` | `0.15s` | `0.15s` | scss/v8-scss/_button.scss | 0 |
| `$button-transition-timing` | `ease-in-out` | `ease-in-out` | scss/v8-scss/_button.scss | 0 |
| `$checkbox-transition-duration` | `0.15s` | `0.15s` | scss/v8-scss/_checkbox.scss | 0 |
| `$checkbox-transition-timing` | `ease-in-out` | `ease-in-out` | scss/v8-scss/_checkbox.scss | 0 |
| `$dropdown-transition` | `0.2s ease` | `0.2s ease` | scss/v8-scss/_dropdownButton.scss | 0 |
| `$dropdown-transition-duration` | `0.15s` | `0.15s` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-transition-timing` | `ease-in-out` | `ease-in-out` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$drp-transition-duration` | `0.2s` | `0.2s` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-transition-timing` | `ease` | `ease` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$filterable-dropdown-transition` | `0.15s ease-in-out` | `0.15s ease-in-out` | scss/v8-scss/_filterableDropdown.scss | 0 |
| `$radio-transition-duration` | `0.15s` | `0.15s` | scss/v8-scss/_radio.scss | 0 |
| `$radio-transition-timing` | `ease-in-out` | `ease-in-out` | scss/v8-scss/_radio.scss | 0 |
| `$search-transition-duration` | `0.2s` | `0.2s` | scss/v8-scss/_search.scss | 0 |
| `$search-transition-timing` | `ease` | `ease` | scss/v8-scss/_search.scss | 0 |
| `$switch-transition-duration` | `0.2s` | `0.2s` | scss/v8-scss/_switch.scss | 0 |
| `$switch-transition-timing` | `ease-in-out` | `ease-in-out` | scss/v8-scss/_switch.scss | 0 |
| `$url-input-transition-duration` | `0.15s` | `0.15s` | scss/v8-scss/_urlInput.scss | 0 |
| `$url-input-transition-timing` | `ease-in-out` | `ease-in-out` | scss/v8-scss/_urlInput.scss | 0 |

### CSS Custom Properties

| Property | Value | Root Block | Source File | Usages |
|----------|-------|------------|-------------|--------|
| - | - | - | - | - |

## Typography

### SCSS Variables

| Variable | Value | Computed | Source File | Usages |
|----------|-------|----------|-------------|--------|
| `$alert-font-size` | `var(--font-size-m)` | `N/A` | scss/v8-scss/_alert.scss | 0 |
| `$alert-font-weight` | `var(--font-weight-medium)` | `N/A` | scss/v8-scss/_alert.scss | 0 |
| `$btn-font-weight` | `bold` | `bold` | scss/_button.scss | 0 |
| `$button-font-size` | `var(--font-size-m)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$button-font-weight` | `var(--font-weight-regular)` | `N/A` | scss/v8-scss/_button.scss | 0 |
| `$deleteTextSize` | `var(--font-size-m)` | `N/A` | scss/v8-scss/_formEditActions.scss | 0 |
| `$deleteTextWeight` | `var(--font-weight-regular)` | `N/A` | scss/v8-scss/_formEditActions.scss | 0 |
| `$dropdown-font-size` | `var(--font-size-m)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-font-weight` | `var(--font-weight-regular)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$dropdown-font-weight-medium` | `var(--font-weight-medium)` | `N/A` | scss/v8-scss/_selectDropdown.scss | 0 |
| `$drp-font-size` | `0.9375rem` | `0.9375rem` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-font-size-small` | `0.875rem` | `0.875rem` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-font-weight` | `400` | `400` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$drp-font-weight-medium` | `500` | `500` | scss/v8-scss/_dateRangePicker.scss | 0 |
| `$filterable-dropdown-font-size` | `14px` | `14px` | scss/v8-scss/_filterableDropdown.scss | 0 |
| `$filterable-dropdown-font-weight` | `var(--font-weight-regular)` | `N/A` | scss/v8-scss/_filterableDropdown.scss | 0 |
| `$filterable-dropdown-font-weight-medium` | `var(--font-weight-medium)` | `N/A` | scss/v8-scss/_filterableDropdown.scss | 0 |
| `$font-size-12` | `var(--font-size-12)` | `N/A` | scss/fileUpload.scss | 0 |
| `$font-size-15` | `var(--font-size-m)` | `N/A` | scss/v8-scss/_tabs.scss | 0 |
| `$font-size-default` | `1.5rem` | `1.5rem` | scss/v8-scss/_breadCrumbs.scss | 0 |
| `$font-size-m` | `var(--font-size-m)` | `N/A` | scss/v8-scss/_variableSelection.scss | 0 |
| `$font-size-minimized` | `0.75rem` | `0.75rem` | scss/v8-scss/_breadCrumbs.scss | 0 |
| `$font-size-xl` | `var(--font-size-xl)` | `N/A` | scss/v8-scss/_mixins.scss | 0 |
| `$font-size-xs` | `var(--font-size-xs)` | `N/A` | scss/fileUpload.scss | 0 |
| `$font-weight-lg` | `var(--font-weight-lg)` | `N/A` | scss/fileUpload.scss | 0 |
| `$font-weight-medium` | `var(--font-weight-medium)` | `N/A` | scss/v8-scss/_variableSelection.scss | 0 |
| `$font-weight-regular` | `var(--font-weight-regular)` | `N/A` | scss/v8-scss/_variableSelection.scss | 0 |
| `$font-weight-sm` | `var(--font-weight-sm)` | `N/A` | scss/fileUpload.scss | 0 |
| `$fontChoiceHead` | `$fontBase*1.25` | `$fontBase*1.25` | scss/_theme.scss | 0 |
| `$fontModalTitle` | `$fontBase*1.5` | `$fontBase*1.5` | scss/_theme.scss | 0 |
| `$fontSectionHead` | `$fontBase*1.125` | `$fontBase*1.125` | scss/_theme.scss | 0 |
| `$fontSmallest` | `$fontBase*0.875` | `$fontBase*0.875` | scss/_theme.scss | 0 |
| `$header-font-size` | `var(--font-size-xl)` | `N/A` | scss/v8-scss/_formCreateLayout.scss | 0 |
| `$header-font-weight` | `var(--font-weight-regular)` | `N/A` | scss/v8-scss/_formCreateLayout.scss | 0 |
| `$headerTextSize` | `var(--font-size-xl)` | `N/A` | scss/v8-scss/_formEditActions.scss | 0 |
| `$headerTextWeight` | `var(--font-weight-medium)` | `N/A` | scss/v8-scss/_formEditActions.scss | 0 |
| `$letter-spacing-default` | `var(--letter-spacing-default)` | `N/A` | scss/v8-scss/_mixins.scss | 0 |
| `$switch-font-size` | `var(--font-size-m)` | `N/A` | scss/v8-scss/_switch.scss | 0 |
| `$ta-font-size` | `var(--font-size-m)` | `N/A` | scss/v8-scss/_textArea.scss | 0 |
| `$ta-font-weight` | `var(--font-weight-regular)` | `N/A` | scss/v8-scss/_textArea.scss | 0 |
| `$ti-font-size` | `var(--font-size-15)` | `N/A` | scss/v8-scss/_textInput.scss | 0 |
| `$ti-font-weight` | `var(--font-weight-regular)` | `N/A` | scss/v8-scss/_textInput.scss | 0 |
| `$url-input-font-size` | `0.9375rem` | `0.9375rem` | scss/v8-scss/_urlInput.scss | 0 |
| `$url-input-font-weight` | `500` | `500` | scss/v8-scss/_urlInput.scss | 0 |

### CSS Custom Properties

| Property | Value | Root Block | Source File | Usages |
|----------|-------|------------|-------------|--------|
| `--default-font-family-url` | `" "` | theme | scss/_theme.scss | 0 |
| `--default-font-size` | `1rem` | theme | scss/_theme.scss | 0 |
| `--font-size-l` | `18px` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--font-size-lg` | `1.5rem` | theme | scss/_theme.scss | 0 |
| `--font-size-m` | `15px` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--font-size-md` | `1.25rem` | theme | scss/_theme.scss | 0 |
| `--font-size-s` | `12px` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--font-size-sm` | `var(--default-font-size)` | theme | scss/_theme.scss | 0 |
| `--font-size-xl` | `20px` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--font-size-xs` | `10px` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--font-weight-lg` | `600` | theme | scss/_theme.scss | 0 |
| `--font-weight-light` | `300` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--font-weight-md` | `500` | theme | scss/_theme.scss | 0 |
| `--font-weight-medium` | `500` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--font-weight-regular` | `400` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--font-weight-semibold` | `600` | v8-theme | scss/v8-scss/_theme.scss | 0 |
| `--font-weight-sm` | `400` | theme | scss/_theme.scss | 0 |
| `--font-weight-xl` | `700` | theme | scss/_theme.scss | 0 |
| `--font-weight-xs` | `300` | theme | scss/_theme.scss | 0 |

## SCSS Maps

### $base-colors

| Key | Value | Computed |
|-----|-------|----------|
| `blue` | `#0087D9` | `#0087D9` |
| `cyan` | `#00BCD4` | `#00BCD4` |
| `green` | `#00C49A` | `#00C49A` |
| `indigo` | `#3248F4` | `#3248F4` |
| `orange` | `#FF9100` | `#FF9100` |
| `red` | `#E57373` | `#E57373` |
| `vivid` | `#7C80FE` | `#7C80FE` |
| `yellow` | `#EFC005` | `#EFC005` |

### $brand-colors

| Key | Value | Computed |
|-----|-------|----------|
| `primary` | `#F1EEFF` | `#F1EEFF` |
| `primary-dark` | `#B8ABFF` | `#B8ABFF` |
| `secondary` | `#EDEDED` | `#EDEDED` |
| `secondary-dark` | `#525254` | `#525254` |
| `vivid` | `#7C80FE` | `#7C80FE` |

### $cursor-map

| Key | Value | Computed |
|-----|-------|----------|
| `cursor-default` | `default` | `default` |
| `cursor-pointer` | `pointer` | `pointer` |

### $custom-colors

| Key | Value | Computed |
|-----|-------|----------|
| `black` | `$black` | `$black` |
| `danger` | `$danger` | `$danger` |
| `gray-dark` | `$gray-dark` | `$gray-dark` |
| `gray-darkest` | `$gray-darkest` | `$gray-darkest` |
| `gray-light` | `$gray-light` | `$gray-light` |
| `gray-medium` | `$gray-medium` | `$gray-medium` |
| `gray-medium-dark` | `$gray-medium-dark` | `$gray-medium-dark` |
| `green` | `$green` | `$green` |
| `primary` | `$primary` | `$primary` |
| `primary-light` | `$primary-light` | `$primary-light` |
| `white` | `$white` | `$white` |

### $font-tokens

| Key | Value | Computed |
|-----|-------|----------|
| `font-family-base` | `'"Figtree"` | `'"Figtree"` |
| `font-size-l` | `18px` | `18px` |
| `font-size-m` | `15px` | `15px` |
| `font-size-s` | `12px` | `12px` |
| `font-size-xl` | `20px` | `20px` |
| `font-size-xs` | `10px` | `10px` |
| `font-weight-light` | `300` | `300` |
| `font-weight-medium` | `500` | `500` |
| `font-weight-regular` | `400` | `400` |
| `font-weight-semibold` | `600` | `600` |
| `letter-spacing-default` | `0%` | `0%` |
| `line-height-default` | `100%` | `100%` |

### $neutral-colors

| Key | Value | Computed |
|-----|-------|----------|
| `gray-dark` | `#7C7D7F` | `#7C7D7F` |
| `gray-darkest` | `#4A4A4A` | `#4A4A4A` |
| `gray-light` | `#D9D9D9` | `#D9D9D9` |
| `gray-medium` | `#D1D2D3` | `#D1D2D3` |
| `gray-medium-dark` | `#B7B7B8` | `#B7B7B8` |
| `gray-medium-darker` | `#9E9E9E` | `#9E9E9E` |
| `gray-x-light` | `#E5E5E5` | `#E5E5E5` |
| `gray-xx-light` | `#DAD9DA` | `#DAD9DA` |
| `white-100` | `#F6F6F6` | `#F6F6F6` |
| `white-200` | `#FCFCFC` | `#FCFCFC` |
| `white-300` | `#FFFFFF` | `#FFFFFF` |

### $opacities

| Key | Value | Computed |
|-----|-------|----------|
| `100` | `1` | `1` |
| `200` | `0.5` | `0.5` |
| `300` | `0.25  // 25%` | `0.25  // 25%` |

### $theme-colors

| Key | Value | Computed |
|-----|-------|----------|
| `black` | `$black` | `$black` |
| `primary` | `$primary` | `$primary` |
| `success` | `$success` | `$success` |
| `white` | `$white` | `$white` |

## Bootstrap Overrides

| Variable | Bootstrap Default | Project Override | Type |
|----------|-------------------|------------------|------|
| `$danger` | `#dc3545` | `var(--default-danger-color)` | color |
| `$primary` | `#007bff` | `var(--ff-primary)` | color |
| `$success` | `#28a745` | `$green-dark` | color |

## Dual :root Blocks

Note: Two :root blocks exist with overlapping properties. The v8-scss/_theme.scss file is loaded after _theme.scss (per index.scss import order), so v8-theme properties take precedence when there are conflicts.

| Property | _theme.scss Value | v8-scss/_theme.scss Value | Active |
|----------|-------------------|---------------------------|--------|
| No overlapping properties found | - | - | - |

## Computed Values (Manual Review Required)

Values that use SCSS functions/expressions and may require manual resolution for token extraction.

| Variable | Expression | Resolved Value | Notes |
|----------|-----------|----------------|-------|
| `$Gray-darkest` | `var(--gray-darkest)` | `manual resolution needed` |  |
| `$Gray-x-light` | `var(--gray-x-light)` | `manual resolution needed` |  |
| `$Secondary` | `var(--secondary)` | `manual resolution needed` |  |
| `$White-200` | `var(--white-200)` | `manual resolution needed` |  |
| `$White-300` | `var(--white-300)` | `manual resolution needed` |  |
| `$alert-font-size` | `var(--font-size-m)` | `manual resolution needed` |  |
| `$alert-font-weight` | `var(--font-weight-medium)` | `manual resolution needed` |  |
| `$alert-gap` | `var(--spacer-050)` | `manual resolution needed` |  |
| `$alert-line-height` | `var(--line-height-default)` | `manual resolution needed` |  |
| `$alert-transition-timing` | `ease-in-out` | `ease-in-out` |  |
| `$black-color` | `var(--gray-darkest)` | `manual resolution needed` |  |
| `$border-radius` | `var(--border-radius)` | `manual resolution needed` |  |
| `$borderRadius` | `var(--border-radius)` | `manual resolution needed` |  |
| `$borderRadiusHeightESM` | `$base*0.78` | `$base*0.78` | $base differs: _theme.scss (0.5rem) vs _variables.scss (1rem) |
| `$borderRadiusHeightL` | `$base*1.594` | `$base*1.594` | $base differs: _theme.scss (0.5rem) vs _variables.scss (1rem) |
| `$borderRadiusHeightM` | `$base*1.344` | `$base*1.344` | $base differs: _theme.scss (0.5rem) vs _variables.scss (1rem) |
| `$borderRadiusHeightSM` | `$base*1.094` | `$base*1.094` | $base differs: _theme.scss (0.5rem) vs _variables.scss (1rem) |
| `$borderRadiusModal` | `$base*1.5` | `$base*1.5` | $base differs: _theme.scss (0.5rem) vs _variables.scss (1rem) |
| `$breadcrumb-transition-timing` | `ease-in-out` | `ease-in-out` |  |
| `$button-font-size` | `var(--font-size-m)` | `manual resolution needed` |  |
| `$button-font-weight` | `var(--font-weight-regular)` | `manual resolution needed` |  |
| `$button-gap` | `var(--spacer-050)` | `manual resolution needed` |  |
| `$button-line-height` | `var(--line-height-default)` | `manual resolution needed` |  |
| `$button-transition-timing` | `ease-in-out` | `ease-in-out` |  |
| `$checkbox-transition-timing` | `ease-in-out` | `ease-in-out` |  |
| `$checkboxSize` | `calc($base + $paddingLvl5S*2)` | `calc($base + $paddingLvl5S*2)` | $base differs: _theme.scss (0.5rem) vs _variables.scss (1rem) |
| `$checkmark-transform` | `translate(-50%, -70%) rotate(45deg) scal` | `translate(-50%, -70%) rotate(45deg) scal` |  |
| `$color-alert-bg` | `var(--white-200)` | `manual resolution needed` |  |
| `$color-alert-border` | `var(--gray-medium-dark)` | `manual resolution needed` |  |
| `$color-alert-error` | `var(--orange-100)` | `manual resolution needed` |  |

*Showing 30 of 257 computed values. See theme-audit.json for complete list.*

## Naming Patterns

Observed naming conventions in the codebase:

### SCSS Variables
- **Convention:** `$kebab-case` (e.g., `$gray-darkest`, `$primary-light`, `$font-base`)
- **Color names:** Descriptive (e.g., `$gray-darkest`, `$primary`, `$green-dark`)
- **Size/spacing:** Base multipliers (e.g., `$base*0.78`, `$fontBase*1.5`)

### CSS Custom Properties
- **Convention:** `--kebab-case` (e.g., `--spacer-100`, `--font-size-xs`)
- **Prefix patterns:**
  - `--ff-*`: Form.io/forms-flow specific properties
  - `--no-code-*`: No-code feature properties
  - No prefix: v8 design system properties
- **Size scales:**
  - Numeric: `--spacer-025` through `--spacer-300` (increments of 25)
  - T-shirt: `--font-size-xs`, `--font-size-sm`, `--font-size-md`, `--font-size-lg`, `--font-size-xl`
  - Opacity variants: `--color-100`, `--color-200`, `--color-300` (100%, 50%, 25%)

### Color Variants
- **Base colors:** 8 base colors (yellow, green, cyan, blue, orange, vivid, red, indigo)
- **Variants:** Each base color has 3 opacity levels (-100, -200, -300)
- **Generated via:** `blend-with-white-to-hex()` function
- **Example:** `--yellow-100` (solid), `--yellow-200` (50%), `--yellow-300` (25%)

## SCSS Mixins

### `@mixin custom-scroll`
- **Source:** forms-flow-theme/scss/v8-scss/_mixins.scss
- **Parameters:** `$width`, `$thumb-height`
- **Design Impact:** Custom scrollbar styling

### `@mixin font-style`
- **Source:** forms-flow-theme/scss/v8-scss/_mixins.scss
- **Parameters:** `$font-size`, `$font-weight`, `$color`
- **Design Impact:** Typography styles using v8 design tokens

### `@mixin generate-overflow`
- **Source:** forms-flow-theme/scss/_variables.scss
- **Parameters:** `$axis`, `$value`
- **Design Impact:** Overflow utility classes

### `@mixin vertical-padding`
- **Source:** forms-flow-theme/scss/v8-scss/_mixins.scss
- **Parameters:** 
- **Design Impact:** Consistent vertical padding for containers

## SCSS Functions

### `@function blend-with-white-to-hex`
- **Source:** forms-flow-theme/scss/v8-scss/_theme.scss
- **Purpose:** Blend colors with white background to achieve opacity variants
- **Design Impact:** Generates 50% and 25% opacity variants of base colors for the v8 design system

## Key Findings

### Version 8 Design System
- **Status:** Partial implementation alongside legacy theme
- **Location:** `v8-scss/` subdirectory
- **Properties:** 79 CSS custom properties in v8 :root block
- **Approach:** Token-based design with systematic color variants

### Legacy Theme
- **Status:** Active, used throughout codebase
- **Location:** Root SCSS files (`_theme.scss`, `_variables.scss`)
- **Properties:** 58 CSS custom properties in theme :root block
- **Characteristics:** Mix of hard-coded values and computed expressions

### Design Token Readiness
- **Direct convertible tokens:** ~345 values
- **Requires computation:** 257 SCSS expressions
- **Bootstrap dependencies:** Need to resolve Bootstrap variable references
- **Dual :root complexity:** Property precedence requires careful handling
