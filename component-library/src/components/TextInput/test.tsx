import * as React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { TextInput } from './index';

it('renders and accepts input', () => {
	const handleChange = jest.fn();
	render(<TextInput label="Name" placeholder="Your name" onChange={handleChange} />);
	const input = screen.getByPlaceholderText('Your name') as HTMLInputElement;
	fireEvent.change(input, { target: { value: 'John' } });
	expect(handleChange).toHaveBeenCalledWith('John');
	expect(input.value).toBe('John');
});
