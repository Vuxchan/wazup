import type { Socket } from "socket.io-client";
import type { Conversation, Message } from "./chat";
import type { Friend, FriendRequest, User } from "./user";

export interface AuthState {
    accessToken: string | null;
    user: User | null;
    loading: boolean;

    setAccessToken: (accessToken: string) => void;

    setUser: (user: User) => void;

    clearState: () => void;

    signUp: (
        username: string,
        password: string,
        email: string,
        firstName: string,
        lastName: string
    ) => Promise<void>; 

    signIn: (
        email: string,
        password: string
    ) => Promise<void>;

    signOut: () => Promise<void>;

    fetchMe: () => Promise<void>;

    refresh: () => Promise<void>;
}

export interface ThemeState {
    isDark: boolean;
    toggleTheme: () => void;
    setTheme: (dark: boolean) => void;
}

export interface ChatState {
    conversations: Conversation[];
    messages: Record<string, {
        items: Message[],
        hasMore: boolean,
        nextCursor?: string | null,
    }>;
    activeConversationId: string | null;
    convoLoading: boolean;
    messageLoading: boolean;
    loading: boolean;
    fakeConversation: Conversation | null;
    setFakeConversation: (conversation: Conversation) => void;
    reset: () => void;
    setActiveConversation: (id: string | null) => void;

    fetchConversations: () => Promise<void>;
    fetchMessages: (conversationId?: string) => Promise<void>;
    sendDirectMessage: (recipientId: string, content: string, imgUrl?: string) => Promise<void>;
    sendGroupMessage: (conversationId: string, content: string, imgUrl?: string) => Promise<void>;

    addMessage: (message: Message) => Promise<void>;
    updateConversation: (conversation: Conversation) => void;
    markAsSeen: () => Promise<void>;
    addConvo: (convo: Conversation, setActiveconvoId: boolean) => void;
    createConversation: (type: "group" | "direct", name: string, memberIds: string[]) => Promise<void>;
}

export interface SocketState {
    socket: Socket | null;
    onlineUsers: string[];
    connectSocket: () => void;
    disconnectSocket: () => void;
}

export interface FriendState {
    friends: Friend[];
    loading: boolean;
    receivedList: FriendRequest[];
    sentList: FriendRequest[];
    searchByUsername: (username: string) => Promise<User | null>; 
    addFriend: (to: string, requestMessage?: string) => Promise<string>;
    getAllFriendRequests: () => Promise<void>;
    acceptRequest: (requestId: string) => Promise<void>;
    declineRequest: (requestId: string) => Promise<void>;
    getFriends: () => Promise<void>;
}

export interface UserState {
    updateAvatarUrl: (formData: FormData) => Promise<void>;
}