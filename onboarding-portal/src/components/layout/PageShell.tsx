'use client';

import { ReactNode } from 'react';
import { StageStepper } from '@/components/navigation/StageStepper';

export function PageShell({ children }: { children: ReactNode }) {
	return (
		<div className="min-h-screen bg-gray-50">
			<div className="flex">
				{/* Sidebar with stage navigation */}
				<div className="w-64 bg-white shadow-sm p-6">
					<h2 className="text-lg font-semibold mb-4">Progress</h2>
					<StageStepper />
				</div>
				
				{/* Main content */}
				<div className="flex-1 p-6">
					{children}
				</div>
			</div>
		</div>
	);
}
