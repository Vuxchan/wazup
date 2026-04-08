import { useAuthStore } from "@/stores/useAuthStore"
import { useChatStore } from "@/stores/useChatStore";
import { useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router";

const ProtectedRoute = () => {
    const { accessToken, user, loading, refresh, fetchMe } = useAuthStore();
    const { fetchConversations } = useChatStore();
    const [starting, setStarting] = useState(true);

    const init = async () => {
        if (!accessToken) {
            await refresh();
        }

        if (accessToken && !user) {
            await fetchMe();
        }

        await fetchConversations();
        setStarting(false);
    }

    useEffect(() => {
        init();
    }, []);

    if (starting || loading) {
        return <div className="flex h-screen items-center justify-center">Loading page...</div>
    }

    if (!accessToken) {
        return (
            <Navigate 
                to="/signin"
                replace
            />
        )
    } 

    return (
        <Outlet></Outlet>
    )
}

export default ProtectedRoute
