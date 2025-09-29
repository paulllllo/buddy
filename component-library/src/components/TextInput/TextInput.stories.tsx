import type { Meta, StoryObj } from '@storybook/react';
import { TextInput } from './index';

const meta: Meta<typeof TextInput> = {
	title: 'Form/TextInput',
	component: TextInput
};

export default meta;

type Story = StoryObj<typeof TextInput>;

export const Default: Story = {
	args: { label: 'Name', placeholder: 'Enter your name' }
};
