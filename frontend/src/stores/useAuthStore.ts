import { create } from "zustand"
import { toast } from "sonner"
import { authService } from "@/services/authService"
import type { AuthState } from "@/types/store"

export const useAuthStore = create<AuthState>((set, get) => ({
    accessToken: null,
    user: null,
    loading: false,

    setAccessToken(accessToken) {
        set({accessToken});
    },

    clearState: () => {
        set({ accessToken: null, user: null, loading: false });
    },

    signUp: async (username, password, email, firstName, lastName) => {
        try {
            set({ loading: true });

            await authService.signUp(username, password, email, firstName, lastName);

            toast.success("Login successful! You will be redirected to the login page.");
        } catch (error) {
            console.error(error);
            toast.error("Login failed");
        } finally {
            set({ loading: false });
        }
    },

    signIn: async (email, password) => {
        try {
            set({ loading: true });

            const response = await authService.signIn(email, password);
            const accessToken = response.access_token;
            get().setAccessToken(accessToken);

            await get().fetchMe();

            toast.success("Welcome back to Moji!");
        } catch (error) {
            console.error(error);
            toast.error("Login failed");
        } finally {
            set({ loading: false });
        }
    },

    signOut: async () => {
        try {
            get().clearState();

            await authService.signOut();

            toast.success("Logout successful!")
        } catch (error) {
            console.error(error);
            toast.error("Logout failed")
        }
    },

    fetchMe: async () => {
        try {
            set({ loading: true })
            const user = await authService.fetchMe();

            set({user});
        } catch (error) {
            console.error(error);
            set({user: null, accessToken: null});
            toast.error("Error while fetching user data. Please try again!");
        } finally {
            set({ loading: false });
        }
    },

    refresh: async () => {
        try {
            set({loading: true})
            const {user, fetchMe} = get();

            const response = await authService.refresh();
            const accessToken = response.access_token;
            get().setAccessToken(accessToken);

            if (!user) {
                await fetchMe();
            }
        } catch (error) {
            console.error(error);
            toast.error("Your session is expired. Please login!")
            get().clearState();
        } finally {
            set({loading: false})
        }
    }
}))