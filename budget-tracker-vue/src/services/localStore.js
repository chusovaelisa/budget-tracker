export function getRefreshToken() {
    return localStorage.getItem("refreshToken") || null;
}

export function setRefreshToken(refreshToken) {
    localStorage.setItem("refreshToken", refreshToken);
}

export function clearRefreshToken() {
    localStorage.removeItem("refreshToken");
}
export function getAccessToken() {
    return localStorage.getItem("accessToken") || null;
}

export function setAccessToken(accessToken) {
    localStorage.setItem("accessToken", accessToken);
}

export function clearAccessToken() {
    localStorage.removeItem("accessToken");
}

