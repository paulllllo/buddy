'use client';

import React from 'react';
import { Header, Description, TextInput, Checklist, Media } from '@kelechi_i/buddy-component-library';

const registry: Record<string, (b: unknown) => React.JSX.Element> = {
	header: (b) => <Header title={b.content?.title} subtitle={b.content?.subtitle} align={b.config?.align} />,
	description: (b) => <Description text={b.content?.text} align={b.config?.align} />,
	text_input: (b) => <TextInput label={b.config?.label} placeholder={b.config?.placeholder} />,
	checklist: (b) => <Checklist items={b.content?.items ?? []} />,
	media: (b) => <Media type={b.config?.mediaType} src={b.content?.src} alt={b.content?.alt} />
};

export function ContentRenderer({ blocks }: { blocks: unknown[] }) {
	return (
		<>
			{blocks.map((b) => (
				<div key={b.id}>{registry[b.type]?.(b) ?? <div>Unsupported: {b.type}</div>}</div>
			))}
		</>
	);
}
