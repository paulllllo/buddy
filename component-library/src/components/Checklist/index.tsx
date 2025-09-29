import * as React from 'react';

export type ChecklistItem = {
	id: string;
	label: string;
	checked?: boolean;
	disabled?: boolean;
};

export type ChecklistProps = {
	items: ChecklistItem[];
	onChange?: (items: ChecklistItem[]) => void;
};

export const Checklist: React.FC<ChecklistProps> = ({ items, onChange }) => {
	const [localItems, setLocalItems] = React.useState<ChecklistItem[]>(items);

	React.useEffect(() => {
		setLocalItems(items);
	}, [items]);

	const toggle = (id: string) => {
		const updated = localItems.map((it) => (it.id === id ? { ...it, checked: !it.checked } : it));
		setLocalItems(updated);
		onChange?.(updated);
	};

	return (
		<ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
			{localItems.map((it) => (
				<li key={it.id} style={{ marginBottom: 8 }}>
					<label>
						<input
							type="checkbox"
							checked={!!it.checked}
							disabled={it.disabled}
							onChange={() => toggle(it.id)}
						/>
						<span style={{ marginLeft: 8 }}>{it.label}</span>
					</label>
				</li>
			))}
		</ul>
	);
};
