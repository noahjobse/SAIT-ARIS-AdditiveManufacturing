import createClient from "openapi-fetch";
import type { paths } from "./types.gen";

// Single shared client — proxied to http://localhost:8000 via Vite config
const client = createClient<paths>({ baseUrl: "/" });

export default client;
