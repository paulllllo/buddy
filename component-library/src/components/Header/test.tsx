import * as React from 'react';
import { render, screen } from '@testing-library/react';
import { Header } from './index';

it('renders title and subtitle', () => {
	render(<Header title="Welcome" subtitle="Start here" />);
	expect(screen.getByRole('heading', { name: 'Welcome' })).toBeInTheDocument();
	expect(screen.getByText('Start here')).toBeInTheDocument();
});
