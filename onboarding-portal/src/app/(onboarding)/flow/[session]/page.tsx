'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { PageShell } from '@/components/layout/PageShell';
import { ContentRenderer } from '@/components/renderer/ContentRenderer';
import { useOnboarding } from '@/lib/context/OnboardingContext';
import toast from 'react-hot-toast';

export default function OnboardingFlowPage() {
	const params = useParams();
	const sessionToken = params.session as string;
	const { state, dispatch } = useOnboarding();
	const [currentStage, setCurrentStage] = useState<{ contentBlocks: unknown[] } | null>(null);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		async function loadSession() {
			try {
				dispatch({ type: 'SET_LOADING', payload: true });
				
				// TODO: Replace with actual service calls when Orval client is generated
				// const session = await onboardingService.getSession(sessionToken);
				// const progress = await onboardingService.getProgress(sessionToken);
				// const stage = await onboardingService.getCurrentStage(sessionToken);
				
				// Mock data for now
				dispatch({ type: 'SET_STAGE_ORDER', payload: ['stage1', 'stage2', 'stage3'] });
				dispatch({ type: 'SET_CURRENT_STAGE', payload: 'stage1' });
				
				setCurrentStage({
					contentBlocks: [
						{ id: '1', type: 'header', content: { title: 'Welcome!', subtitle: 'Let\'s get started' } },
						{ id: '2', type: 'description', content: { text: 'This is your onboarding journey.' } },
						{ id: '3', type: 'text_input', config: { label: 'Your Name', placeholder: 'Enter your name' } }
					]
				});
				
			} catch {
				dispatch({ type: 'SET_ERROR', payload: 'Failed to load onboarding session' });
				toast.error('Failed to load onboarding session');
			} finally {
				setLoading(false);
				dispatch({ type: 'SET_LOADING', payload: false });
			}
		}

		if (sessionToken) {
			loadSession();
		}
	}, [sessionToken, dispatch]);

	if (loading) {
		return (
			<PageShell>
				<div className="flex items-center justify-center h-64">
					<div className="text-lg">Loading...</div>
				</div>
			</PageShell>
		);
	}

	if (state.error) {
		return (
			<PageShell>
				<div className="text-red-600">{state.error}</div>
			</PageShell>
		);
	}

	return (
		<PageShell>
			<div className="max-w-2xl mx-auto">
				<div className="bg-white rounded-lg shadow-sm p-6">
					<h1 className="text-2xl font-bold mb-6">Onboarding Flow</h1>
					
					{currentStage && (
						<ContentRenderer blocks={currentStage.contentBlocks} />
					)}
					
					<div className="mt-8 flex justify-between">
						<button className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300">
							Previous
						</button>
						<button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
							Save
						</button>
						<button className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">
							Next
						</button>
					</div>
				</div>
			</div>
		</PageShell>
	);
}
