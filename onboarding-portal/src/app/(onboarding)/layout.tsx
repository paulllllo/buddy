'use client';

import { OnboardingProvider } from '@/lib/context/OnboardingContext';
import { Toaster } from 'react-hot-toast';

export default function OnboardingLayout({
	children,
}: {
	children: React.ReactNode;
}) {
	return (
		<OnboardingProvider>
			<Toaster position="top-right" />
			{children}
		</OnboardingProvider>
	);
}
