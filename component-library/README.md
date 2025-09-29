# @kelechi_i/buddy-component-library

Reusable React component library for the OaaS app.

## Install

```bash
pnpm add @kelechi_i/buddy-component-library
```

Peer deps required in host app:
- react >=18
- react-dom >=18

## Build

```bash
pnpm build
```

## Storybook

```bash
pnpm storybook
```

## Test

```bash
pnpm test
```

## Usage

```tsx
import { Header, Description, TextInput, Checklist, Media } from '@kelechi_i/buddy-component-library';

export default function Example() {
	return (
		<div>
			<Header title="Welcome" subtitle="Start here" align="center" />
			<Description text="A simple description" />
			<TextInput label="Name" placeholder="Enter your name" />
			<Checklist items={[{ id: '1', label: 'Read handbook' }]} />
			<Media type="image" src="https://via.placeholder.com/400x200" />
		</div>
	);
}
```
