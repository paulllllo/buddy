import * as React from 'react';

export type MediaProps = {
	type: 'image' | 'video';
	src: string;
	alt?: string;
	controls?: boolean;
	width?: number | string;
	height?: number | string;
	style?: React.CSSProperties;
};

export const Media: React.FC<MediaProps> = ({ type, src, alt, controls = true, width = '100%', height, style }) => {
	if (type === 'image') {
		return <img src={src} alt={alt ?? ''} style={{ width, height, ...style }} />;
	}
	return (
		<video src={src} controls={controls} style={{ width, height, ...style }}>
			{alt ? <track kind="captions" label={alt} /> : null}
		</video>
	);
};
