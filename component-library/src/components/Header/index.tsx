import * as React from 'react';

export type HeaderProps = {
	title: string;
	subtitle?: string;
	align?: 'left' | 'center' | 'right';
};

export const Header: React.FC<HeaderProps> = ({ title, subtitle, align = 'left' }) => {
	return (
		<div style={{ textAlign: align }}>
			<h1>{title}</h1>
			{subtitle ? <p>{subtitle}</p> : null}
		</div>
	);
};
