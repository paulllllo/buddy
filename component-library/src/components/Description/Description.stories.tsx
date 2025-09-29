import type { Meta, StoryObj } from '@storybook/react';
import { Description } from './index';

const meta: Meta<typeof Description> = {
	title: 'Content/Description',
	component: Description
};

export default meta;

type Story = StoryObj<typeof Description>;

export const Default: Story = {
	args: { text: 'This is a description paragraph.', align: 'left' }
};
