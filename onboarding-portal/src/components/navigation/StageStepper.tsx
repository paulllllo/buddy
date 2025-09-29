'use client';

import { useOnboarding } from '@/lib/context/OnboardingContext';

export function StageStepper() {
	const { state } = useOnboarding();
	
	return (
		<div className="space-y-2">
			{state.stageOrder.map((stageId, index) => (
				<div key={stageId} className="flex items-center space-x-2">
					<div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
						stageId === state.currentStageId 
							? 'bg-blue-500 text-white' 
							: 'bg-gray-200 text-gray-600'
					}`}>
						{index + 1}
					</div>
					<span className="text-sm">Stage {index + 1}</span>
				</div>
			))}
		</div>
	);
}
