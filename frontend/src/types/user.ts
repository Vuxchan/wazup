export interface User {
    id: string;
    username: string;
    email: string;
    displayName: string;
    avatarUrl?: string;
    bio?: string;
    phone?: string;
    createdAt?: string;
    updatedAt?: string;
}

export interface Friend {
    id: string;
    username: string;
    displayName: string;
    avatarUrl?: string;
}

export interface FriendRequest {
    id: string;
    fromUser?: {
        id: string;
        username: string;
        displayName: string;
        avatarUrl?: string;
    }
    toUser?: {
        id: string;
        username: string;
        displayName: string;
        avatarUrl?: string;
    }
    requestMessage: string;
    createdAt: string;
    updatedAt: string;
}