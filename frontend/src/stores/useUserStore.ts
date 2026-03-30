import type { UserState } from "@/types/store";
import { create } from "zustand";
import { useAuthStore } from "./useAuthStore";
import { userService } from "@/services/userService";
import { toast } from "sonner";
import { useChatStore } from "./useChatStore";

export const useUserStore = create<UserState>(() => ({
    updateAvatarUrl: async (formData) => {
        try {
            const {user, setUser} = useAuthStore.getState();
            const data = await userService.uploadAvatar(formData);

            if (user) {
                setUser({
                    ...user,
                    avatarUrl: data,
                });

                useChatStore.getState().fetchConversations();
            }
        } catch (error) {
            console.error("Error while updating avatar url", error);
            toast.error("Uploading avatar failed!");
        }
    }
}))