import type { Meta, StoryObj } from '@storybook/react';
import { Media } from './index';

const meta: Meta<typeof Media> = {
	title: 'Content/Media',
	component: Media
};

export default meta;

type Story = StoryObj<typeof Media>;

export const Image: Story = {
	args: { type: 'image', src: 'https://via.placeholder.com/400x200', alt: 'Placeholder' }
};

export const Video: Story = {
	args: { type: 'video', src: 'https://www.w3schools.com/html/mov_bbb.mp4', alt: 'Sample video' }
};
