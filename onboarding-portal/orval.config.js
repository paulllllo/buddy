module.exports = {
	backend: {
		input: 'http://localhost:8000/openapi.json',
		output: {
			target: 'src/lib/api/index.ts',
			client: 'axios',
			override: {
				mutator: {
					path: 'src/lib/axios/axiosInstance.ts',
					name: 'customAxios'
				}
			}
		}
	}
};
