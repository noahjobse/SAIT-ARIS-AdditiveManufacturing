import { NextRequest, NextResponse } from "next/server";

export function proxy(request: NextRequest) {
  const hostname = request.headers.get("host") ?? "";
  const isAppSubdomain = hostname.startsWith("app.");

  if (isAppSubdomain) {
    const url = request.nextUrl.clone();
    // Rewrite app.armstudio.com/* → /app/*
    if (!url.pathname.startsWith("/app")) {
      url.pathname = "/app" + url.pathname;
      return NextResponse.rewrite(url);
    }
  }

  return NextResponse.next();
}

export const proxyConfig = {
  matcher: ["/((?!_next|api|.*\\..*).*)"],
};
