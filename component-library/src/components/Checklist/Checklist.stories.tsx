import type { Meta, StoryObj } from '@storybook/react';
import { Checklist } from './index';

const meta: Meta<typeof Checklist> = {
	title: 'Form/Checklist',
	component: Checklist
};

export default meta;

type Story = StoryObj<typeof Checklist>;

export const Default: Story = {
	args: {
		items: [
			{ id: '1', label: 'Read handbook' },
			{ id: '2', label: 'Sign NDA', checked: true }
		]
	}
};
