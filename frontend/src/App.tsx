import {BrowserRouter, Route, Routes} from "react-router"
import SignInPage from "./pages/SigninPage";
import SignUpPage from "./pages/SignupPage";
import ChatAppPage from "./pages/ChatAppPage";
import {Toaster} from "sonner"
import ProtectedRoute from "./components/auth/ProtectedRoute";
import { TooltipProvider } from "./components/ui/tooltip";
import { useThemeStore } from "./stores/useThemeStore";
import { useEffect } from "react";
import { useAuthStore } from "./stores/useAuthStore";
import { useSocketStore } from "./stores/useSocketStore";

function App() {
    const {isDark, setTheme} = useThemeStore();
    const {accessToken} = useAuthStore();
    const {connectSocket, disconnectSocket} = useSocketStore();

    useEffect(() => {
        setTheme(isDark);
    }, [isDark]);

    useEffect(() => {
        if (accessToken) {
            connectSocket();
        }

        return () => disconnectSocket();
    }, [accessToken]);

    return <>
        <TooltipProvider>
            <Toaster/>
            <BrowserRouter>
                <Routes>
                    {/* public routes */}
                    <Route
                        path='/signin'
                        element={<SignInPage/>}
                    />

                    <Route
                        path='/signup'
                        element={<SignUpPage/>}
                    />

                    {/* protected routes */}
                    <Route element={<ProtectedRoute/>}>
                        <Route
                            path='/'
                            element={<ChatAppPage/>}
                        />
                    </Route>

                </Routes>
            </BrowserRouter>
        </TooltipProvider>
    </>;
}

export default App
