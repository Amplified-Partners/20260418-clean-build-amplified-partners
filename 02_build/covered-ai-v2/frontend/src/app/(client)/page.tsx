/**
 * Client App - Root Redirect
 * 
 * Redirects to /home
 */

import { redirect } from "next/navigation";

export default function ClientRootPage() {
  redirect("/home");
}
