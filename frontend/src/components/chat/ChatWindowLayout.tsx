import { useChatStore } from "@/stores/useChatStore"
import ChatWelcomeScreen from "./ChatWelcomeScreen";
import ChatWindowSkeleton from "./ChatWindowSkeleton";
import { SidebarInset } from "../ui/sidebar";
import ChatWindowHeader from "./ChatWindowHeader";
import ChatWindowBody from "./ChatWindowBody";
import MessageInput from "./MessageInput";
import { useEffect, useRef } from "react";


const ChatWindowLayout = () => {
	const {activeConversationId, conversations, messageLoading: loading, markAsSeen, fakeConversation} = useChatStore();
	const markingRef = useRef(false);

	const selectedConvo = conversations.find((c) => c.id === activeConversationId) ?? (fakeConversation ?? null);

	useEffect(() => {
		if (!selectedConvo) {
			return;
		}

		if (markingRef.current) return;

		markingRef.current = true;

		const markSeen = async () => {
			try {
				await markAsSeen();
			} catch (error) {
				console.error("Error in markSeen", error);
			} finally {
				markingRef.current = false;
			}
		}

		markSeen();
	}, [markAsSeen, selectedConvo])

	if (!selectedConvo) {
		return <ChatWelcomeScreen />
	}

	if (loading) {
		return <ChatWindowSkeleton />
	}
   
	return (
		<SidebarInset className="flex flex-col h-full flex-1 overflow-hidden rounded-sm shadow-md">
			{/* Header */}
			<ChatWindowHeader chat={selectedConvo}/>

			{/* Body */}
			<div className="flex-1 overflow-y-auto bg-primary-foreground">
				<ChatWindowBody />
			</div>

			{/* Footer */}
			<MessageInput selectedConvo={selectedConvo}/>
		</SidebarInset>
	)
}

export default ChatWindowLayout
