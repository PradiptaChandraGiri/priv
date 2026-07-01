---
name: Kinetic Engineering Portfolio
colors:
  surface: '#13131b'
  surface-dim: '#13131b'
  surface-bright: '#393841'
  surface-container-lowest: '#0d0d15'
  surface-container-low: '#1b1b23'
  surface-container: '#1f1f27'
  surface-container-high: '#292932'
  surface-container-highest: '#34343d'
  on-surface: '#e4e1ed'
  on-surface-variant: '#c7c4d7'
  inverse-surface: '#e4e1ed'
  inverse-on-surface: '#303038'
  outline: '#908fa0'
  outline-variant: '#464554'
  surface-tint: '#c0c1ff'
  primary: '#c0c1ff'
  on-primary: '#1000a9'
  primary-container: '#8083ff'
  on-primary-container: '#0d0096'
  inverse-primary: '#494bd6'
  secondary: '#d0bcff'
  on-secondary: '#3c0091'
  secondary-container: '#571bc1'
  on-secondary-container: '#c4abff'
  tertiary: '#ffb783'
  on-tertiary: '#4f2500'
  tertiary-container: '#d97721'
  on-tertiary-container: '#452000'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e1e0ff'
  primary-fixed-dim: '#c0c1ff'
  on-primary-fixed: '#07006c'
  on-primary-fixed-variant: '#2f2ebe'
  secondary-fixed: '#e9ddff'
  secondary-fixed-dim: '#d0bcff'
  on-secondary-fixed: '#23005c'
  on-secondary-fixed-variant: '#5516be'
  tertiary-fixed: '#ffdcc5'
  tertiary-fixed-dim: '#ffb783'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#703700'
  background: '#13131b'
  on-background: '#e4e1ed'
  surface-variant: '#34343d'
typography:
  display-lg:
    fontFamily: Poppins
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Poppins
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Poppins
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.0'
    letterSpacing: 0.05em
  code-block:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.7'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1280px
  gutter: 24px
  margin-desktop: 64px
  margin-mobile: 20px
  unit-xs: 4px
  unit-sm: 8px
  unit-md: 16px
  unit-lg: 24px
  unit-xl: 48px
---

## Brand & Style

This design system is engineered for high-achieving BTech students, blending academic rigor with cutting-edge technical flair. The brand personality is **Professional, Innovative, and Precise**. It seeks to evoke a sense of "High-Fidelity Engineering"—where clean code meets polished presentation.

The aesthetic utilizes **Glassmorphism** as its primary structural driver, using translucent layers to create a sense of depth and modernity. In Dark Mode, the interface transitions into a "Command Center" feel, utilizing Indigo glows and subtle gradients to highlight key technical achievements. Transitions should be fluid and purposeful, mimicking the smooth execution of optimized algorithms.

## Colors

The palette is anchored by a sophisticated duo of **Indigo** and **Violet**, representing the intersection of logic and creativity. 

- **Primary (Indigo):** Used for main actions, active states, and primary brand markers.
- **Secondary (Violet):** Used for decorative accents, hover states, and progressive disclosure elements.
- **Accent (Cyan):** Reserved for technical highlights, "Live" status indicators, and data visualization points.
- **Surface Strategy:** In Dark Mode, surfaces use the Deep Navy (#0b0f1a) with varying levels of opacity and blur. Light Mode uses a crisp Gray-50 (#f9fafb) for maximum readability.

## Typography

The typographic hierarchy prioritizes clarity and technical authority. 
- **Headings:** Poppins provides a geometric, modern structure for display text, ensuring project titles feel impactful.
- **Body:** Inter is utilized for its exceptional legibility at small sizes, particularly for long-form project descriptions and resumes.
- **Code:** JetBrains Mono is the dedicated choice for snippets, terminal outputs, and technical specifications, signaling a "developer-first" mindset.

Use `display-lg` for hero sections, ensuring it scales down to `display-lg-mobile` on smaller viewports to maintain visual balance.

## Layout & Spacing

The layout follows a **12-column fluid grid** for desktop and a **4-column grid** for mobile. 

- **Grid Logic:** Use 24px gutters to allow the glassmorphic card edges enough breathing room to display their backdrop blurs effectively.
- **Vertical Rhythm:** Spacing between sections should be generous (unit-xl) to emphasize the premium, editorial feel of a portfolio.
- **Responsive Behavior:** On mobile, margins reduce to 20px, and complex grids (like project galleries) should stack vertically to maintain readability and touch targets.

## Elevation & Depth

Depth is conveyed through **Glassmorphism** rather than traditional opaque shadows.

- **The Glass Effect:** Base surfaces use a background blur (12px to 20px) with a semi-transparent white (Light Mode) or navy (Dark Mode) fill at 10-15% opacity.
- **Borders:** Every glass element must have a 1px "inner-light" border (e.g., White at 20% opacity on top/left) to simulate light catching the edge of the glass.
- **Indigo Glows:** In Dark Mode, high-priority elements (like the 'Hire Me' button or a Featured Project) use a soft, diffused outer glow of `rgba(99, 102, 241, 0.3)` with a 30px spread.

## Shapes

The design system uses a sophisticated "Rounded" profile. 
- **Standard UI (Buttons, Inputs):** 12px (md) for a friendly yet professional appearance.
- **Cards & Containers:** 16px (lg) for a distinct separation from the background.
- **Hero Sections / Large Containers:** 24px (xl) to create a focal point.
- **Interactive States:** Hovering over a card should trigger a slight increase in perceived depth (via border intensity) rather than a change in shape.

## Components

### Buttons
- **Primary:** Solid Indigo background with a subtle Violet gradient. On hover, apply an Indigo glow.
- **Secondary:** Transparent with a 1px Indigo border. Glass blur background.
- **Text:** Uppercase Inter, 14px, Semi-bold.

### Cards (Project & Skills)
- **Base:** Glassmorphic background (16px radius). 
- **Header:** Project title in Poppins 20px. 
- **Footer:** Skill chips and GitHub/Live Link icons.
- **Animation:** 0.3s ease-in-out lift on hover with a slight opacity increase of the backdrop blur.

### Chips (Tech Stack)
- **Style:** Small, pill-shaped containers with a background of `rgba(6, 182, 212, 0.1)` (Cyan) and Cyan text. 
- **Typography:** JetBrains Mono 12px for a technical feel.

### Input Fields & Terminal
- **Inputs:** 12px radius, dark navy background (Dark Mode), Indigo focus ring.
- **Terminal Component:** A custom container for the "About Me" or "Experience" section. Darker than standard cards, featuring a "macOS style" window header (red, yellow, green dots) and JetBrains Mono text.

### Progress Bars (Skills)
- **Track:** 8px height, 10% Indigo background.
- **Fill:** Gradient from Indigo to Cyan, indicating a "Technical Loading" state.