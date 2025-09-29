import * as React from 'react';

export type DescriptionProps = {
	text: string;
	align?: 'left' | 'center' | 'right';
};

export const Description: React.FC<DescriptionProps> = ({ text, align = 'left' }) => {
	return <p style={{ textAlign: align }}>{text}</p>;
};
