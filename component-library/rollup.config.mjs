import path from 'node:path';
import typescript from '@rollup/plugin-typescript';
import commonjs from '@rollup/plugin-commonjs';
import nodeResolve from '@rollup/plugin-node-resolve';
import postcss from 'rollup-plugin-postcss';

/** @type {import('rollup').RollupOptions} */
const config = {
	input: 'src/index.ts',
	external: ['react', 'react-dom'],
	output: [
		{
			file: 'dist/index.esm.js',
			format: 'esm',
			sourcemap: true
		},
		{
			file: 'dist/index.cjs.js',
			format: 'cjs',
			sourcemap: true,
			exports: 'named'
		}
	],
	plugins: [
		nodeResolve({ extensions: ['.js', '.jsx', '.ts', '.tsx'] }),
		commonjs(),
		postcss({ extract: path.resolve('dist/styles.css') }),
		typescript({ tsconfig: './tsconfig.json' })
	]
};

export default config;
