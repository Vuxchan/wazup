import { friendService } from "@/services/friendService";
import type { FriendState } from "@/types/store";
import { create } from "zustand";

export const useFriendStore = create <FriendState>((set) => ({
    friends: [],
    loading: false,
    receivedList: [],
    sentList: [],
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
    },
    getAllFriendRequests: async () => {
        try {
            set({loading: true});

            const result = await friendService.getAllFriendRequest();

            if (!result) return;

            const {received, sent} = result;

            set({receivedList: received, sentList: sent});
        } catch (error) {
            console.error("Error while getting all friend requests", error);   
        } finally {
            set({loading: false});
        }
    },
    acceptRequest: async (requestId) => {
        try {
            set({loading: true});

            await friendService.acceptRequest(requestId);

            set((state) => ({
                receivedList: state.receivedList.filter((r) => r.id !== requestId),
            }));
        } catch (error) {
           console.error("Error while accepting request", error);   
        } finally {
            set({loading: false});
        }
    },
    declineRequest: async (requestId) => {
        try {
            set({loading: true});

            await friendService.declineRequest(requestId);

            set((state) => ({
                receivedList: state.receivedList.filter((r) => r.id !== requestId),
            }));
        } catch (error) {
           console.error("Error while declining request", error);   
        } finally {
            set({loading: false});
        }
    },
    getFriends: async () => {
        try {
            set({loading: true});
            const friends = await friendService.getFriendList();
            set({friends: friends});
        } catch (error) {
            console.error("Error while getting all friends", error);
            set({friends: []});
        } finally {
            set({loading: false});
        }
    },
}))