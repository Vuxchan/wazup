export interface Participant {
    id: string;
    displayName: string;
    avatarUrl?: string | null;
    joinedAt: string;
}

export interface SeenUser {
    _id: string;    
    displayName?: string;
    avatarUrl?: string | null;
}

export interface Group {
    name: string;
    createdBy: string;
}

export interface LastMessage {
    id: string;    
    content: string;
    createdAt: string;
    sender: {
        id: string;
        displayName: string;
        avatarUrl?: string | null;
    };
}

export interface Conversation {
    id: string;   
    type: "direct" | "group";
    group: Group; 
    participants: Participant[];
    lastMessageAt: string;
    seenBy: SeenUser[];
    lastMessage: LastMessage | null;
    unreadCounts: Record<string, number>;
    createdAt: string;
    updatedAt: string;
}

export interface ConversationResponse {
    conversations: Conversation[];
}

export interface Message {
    id: string;
    conversationId: string;
    senderId: string;
    content: string | null;
    imgUrl?: string | null;
    updatedAt?: string | null;
    createdAt: string;
    isOwn?: boolean;
}