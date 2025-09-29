import * as React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Checklist } from './index';

it('toggles checklist items', () => {
	const onChange = jest.fn();
	render(
		<Checklist
			items={[
				{ id: '1', label: 'Item 1', checked: false },
				{ id: '2', label: 'Item 2', checked: true }
			]}
			onChange={onChange}
		/>
	);
	const first = screen.getByLabelText('Item 1') as HTMLInputElement;
	fireEvent.click(first);
	expect(onChange).toHaveBeenCalled();
});
