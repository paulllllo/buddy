# Onboarding Portal Implementation Plan (Axios + React Context)

This plan describes the standalone Onboarding Portal frontend that consumes the backend API and renders flows dynamically using the published component library `@kelechi_i/buddy-component-library`.

## 1) Goals
- Load an onboarding session via a session token in the URL and render the assigned flow.
- Display all stages and progress; allow Previous/Next navigation.
- Dynamically render stage content types using our component library and backend-provided config/content.
- Strong separation of concerns: generated API client (Orval) → services layer → UI.

## 2) Technology Choices
- Framework: Next.js (TypeScript, App Router)
- Styling: Tailwind CSS
- Requests: Axios (no React Query). Orval will generate Axios-based clients, wired to a custom Axios instance.
- State Management: React Context + useReducer/useState (no Zustand/Redux/React Query)
- Forms (when needed): React Hook Form
- Components: `@kelechi_i/buddy-component-library`

## 3) Project Structure
```
onboarding-portal/
├── app/
│   ├── (onboarding)/flow/[session]/page.tsx      # Entry route using session token
│   ├── (onboarding)/layout.tsx                   # Shell layout with stage nav
│   └── globals.css
├── components/
│   ├── layout/PageShell.tsx
│   ├── navigation/StageStepper.tsx
│   └── renderer/ContentRenderer.tsx
├── lib/
│   ├── api/                                      # Orval output (axios-based)
│   ├── axios/axiosInstance.ts                    # Custom Axios instance
│   ├── services/
│   │   ├── onboardingService.ts                  # Wraps generated api; UI-friendly funcs
│   │   └── progressService.ts                    # Local progress helpers/mapping
│   ├── context/
│   │   └── OnboardingContext.tsx                 # React Context for portal UI state
│   ├── models/                                   # UI models + mappers
│   └── utils/                                    # helpers
├── orval.config.js
├── tailwind.config.ts
├── postcss.config.js
└── package.json
```

## 4) Data Flow (Session → UI)
- URL: `/flow/[session]` where `[session]` is the session token.
- On route load, the page uses the services layer to:
  - getSession: GET `/onboarding/{session_token}`
  - getProgressOverview: GET `/onboarding/{session_token}/progress`
  - getCurrentStage: GET `/onboarding/{session_token}/current-stage`
  - getStageWithBlocks: GET `/onboarding/{session_token}/stages/{stage_id}`
- On interactions:
  - completeContentBlock(on save click): POST `/onboarding/{session_token}/stages/{stage_id}/content-blocks/{content_block_id}/complete`
  - completeStage: POST `/onboarding/{session_token}/stages/{stage_id}/complete`

## 5) Orval + Axios (no React Query)
- Orval generates TypeScript api and types with the axios generator.
- Use a custom axios instance for baseURL, headers, error handling, and token injection.

Example `orval.config.js` (concept):
```js
module.exports = {
	backend: {
		input: 'http://localhost:8000/openapi.json',
		output: {
			target: 'lib/api/index.ts',
			client: 'axios',
			override: {
				mutator: {
					path: 'lib/axios/axiosInstance.ts',
					name: 'customAxios'
				}
			}
		}
	}
};
```

Example `axiosInstance.ts` (concept):
```ts
import axios from 'axios';

export const customAxios = ({ baseURL, ...config } = {}) => {
	const instance = axios.create({ baseURL: baseURL ?? process.env.NEXT_PUBLIC_API_URL, ...config });
	instance.interceptors.request.use((req) => {
		// attach token/cookies if needed
		return req;
	});
	instance.interceptors.response.use(
		(res) => res,
		(err) => Promise.reject(err)
	);
	return instance;
};
```

## 6) Services Layer (UI-friendly API)
- `onboardingService.ts`
  - `getSession(sessionToken)`
  - `getProgress(sessionToken)`
  - `getCurrentStage(sessionToken)`
  - `getStage(sessionToken, stageId)`
  - `completeContentBlock(sessionToken, stageId, contentBlockId, data)`
  - `completeStage(sessionToken, stageId)`
- `progressService.ts`
  - `computeProgress(overview)` → percentage, currentIndex
  - `isStageComplete(stage)`

Services import only the Orval-generated axios client and return UI models or raw data mapped for UI.

## 7) React Context for UI State
- `OnboardingContext` holds minimal UI state not owned by the server (e.g., selected stage id, transient UI flags).
- Data fetching remains request/response per user actions via services. The Context can cache the last responses if needed, but avoid duplicating server truth.

Example shape:
```ts
export type OnboardingState = {
	stageOrder: string[];
	currentStageId?: string;
	loading: boolean;
	error?: string;
};
```

## 8) Dynamic Content Rendering
- `ContentRenderer` takes `contentBlocks` and renders using library components via a registry mapping.
- Mapping translates backend `config`/`content` → library props.

Registry example (concept):
```tsx
import { Header, Description, TextInput, Checklist, Media } from '@kelechi_i/buddy-component-library';

const registry: Record<string, (b: any) => JSX.Element> = {
	header: (b) => <Header title={b.content?.title} subtitle={b.content?.subtitle} align={b.config?.align} />,
	description: (b) => <Description text={b.content?.text} align={b.config?.align} />,
	text_input: (b) => <TextInput label={b.config?.label} placeholder={b.config?.placeholder} />,
	checklist: (b) => <Checklist items={b.content?.items ?? []} />,
	media: (b) => <Media type={b.config?.mediaType} src={b.content?.src} alt={b.content?.alt} />
};

export function ContentRenderer({ blocks }: { blocks: any[] }) {
	return (
		<>
			{blocks.map((b) => (
				<div key={b.id}>{registry[b.type]?.(b) ?? <div>Unsupported: {b.type}</div>}</div>
			))}
		</>
	);
}
```

## 9) Navigation & Progress
- `StageStepper` shows all stages with indicators: completed/current/pending.
- Controls:
  - Prev: navigate to previous stage id in order.
  - Complete Stage: calls service; refresh current/next.
  - Next: navigate to next stage id (only if stage is complete, per rules).
  - Save: Saves the current state of the stage by senfing user info to the content complete endpoint.
- Guard: disable Next until required content blocks are completed.

## 10) Pages & Layout
- `page.tsx` in `/flow/[session]`:
  - Parse `session` param.
  - Call services to fetch session, progress, current stage; show loading/error states.
  - Render `StageStepper`, `ContentRenderer`, and control buttons.
- `layout.tsx` provides a responsive shell; stages at the side on desktop, top on mobile.

## 11) Error & Loading
- Inline loaders (skeletons/spinners) during requests.
- Add toast to properly display error and success messages to user. Use a toast package.

## 12) Testing Strategy
- Unit: services and mapping functions; ContentRenderer registry.
- Integration: `/flow/[session]` page with mocked services for navigation and completion.

## 13) Scripts
- `pnpm add @kelechi_i/buddy-component-library axios orval`
- `pnpm run api:generate` (Orval)
- `pnpm dev` (Next.js)
- `pnpm build` (Next.js)

## 14) Milestones
- Milestone 1: Setup
  - Next.js + Tailwind initialized
  - Orval configured (axios client + custom axios mutator)
  - Install component library
- Milestone 2: Core UI
  - Context provider and shell layout
  - Stage stepper and content renderer
  - `/flow/[session]` page wiring
- Milestone 3: Interactions
  - Complete content block and stage flows
  - Prev/Next navigation and guards
- Milestone 4: Polish & Tests
  - Loading/error states
  - Unit/integration tests
  - Accessibility and responsive refinements
