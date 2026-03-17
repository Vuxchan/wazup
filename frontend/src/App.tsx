import {BrowserRouter, Route, Routes} from "react-router"
import SignInPage from "./pages/SigninPage";
import SignUpPage from "./pages/SignupPage";
import ChatAppPage from "./pages/ChatAppPage";
import {Toaster} from "sonner"
import ProtectedRoute from "./components/auth/ProtectedRoute";
import { TooltipProvider } from "./components/ui/tooltip";
import { useThemeStore } from "./stores/useThemeStore";
import { useEffect } from "react";

function App() {
    const {isDark, setTheme} = useThemeStore();

    useEffect(() => {
        setTheme(isDark);
    }, [isDark]);

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
