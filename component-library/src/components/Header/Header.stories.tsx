import type { Meta, StoryObj } from '@storybook/react';
import { Header } from './index';

const meta: Meta<typeof Header> = {
	title: 'Content/Header',
	component: Header
};

export default meta;

type Story = StoryObj<typeof Header>;

export const Default: Story = {
	args: { title: 'Welcome', subtitle: 'Start here', align: 'left' }
};

export const Centered: Story = {
	args: { title: 'Centered', subtitle: 'Subtitle', align: 'center' }
};
