import * as React from 'react';

export type TextInputProps = {
	label?: string;
	placeholder?: string;
	value?: string;
	onChange?: (value: string) => void;
	required?: boolean;
	disabled?: boolean;
};

export const TextInput: React.FC<TextInputProps> = ({
	label,
	placeholder,
	value,
	onChange,
	required,
	disabled
}) => {
	const [internalValue, setInternalValue] = React.useState<string>(value ?? '');

	React.useEffect(() => {
		if (value !== undefined) setInternalValue(value);
	}, [value]);

	const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const next = e.target.value;
		setInternalValue(next);
		onChange?.(next);
	};

	return (
		<label style={{ display: 'block' }}>
			{label ? <span style={{ display: 'block', marginBottom: 4 }}>{label}{required ? ' *' : ''}</span> : null}
			<input
				type="text"
				placeholder={placeholder}
				value={internalValue}
				onChange={handleChange}
				disabled={disabled}
				style={{ width: '100%', padding: '8px 10px' }}
			/>
		</label>
	);
};
