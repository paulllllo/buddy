/** @type {import('jest').Config} */
module.exports = {
	preset: 'ts-jest',
	testEnvironment: 'jsdom',
	roots: ['<rootDir>/src'],
	moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx'],
	transform: {
		'^.+\\.(t|j)sx?$': 'ts-jest'
	},
	moduleNameMapper: {
		'^@/components/(.*)$': '<rootDir>/src/components/$1',
		'\\.(css|less|scss)$': '<rootDir>/test-utils/styleMock.js'
	},
	setupFilesAfterEnv: ['<rootDir>/setupTests.ts']
};
