import { friendService } from "@/services/friendService";
import type { FriendState } from "@/types/store";
import { use } from "react";
import { create } from "zustand";

export const useFriendStore = create <FriendState>((set, get) => ({
    loading: false,
    searchByUsername: async (username) => {
        try {
            set({loading: true});

            const user = await friendService.searchByUsername(username);

            return user;
        } catch (error) {
            console.error("Error while seaching user by username", error);
            return null;
        } finally {
            set({loading: false})
        }
    },
    addFriend: async (to, requestMessage) => {
        try {
            set({loading: true});
            const resultMessage = await friendService.sendFriendRequest(to, requestMessage);
            return resultMessage;
        } catch (error) {
            console.error("Error while adding friend", error);
        } finally {
            set({loading: false})
        }
    }
}))