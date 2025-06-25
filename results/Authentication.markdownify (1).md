# Authentication

---

Hospitable protects our API endpoints using Personal Access Tokens, and [OAuth 2.0](https://tools.ietf.org/html/rfc6749)'s Authorization flow grants. Depending on your application use case, it might depend which authentication grant you choose to go with.

### [What Authentication should I use?](#what-authentication-should-i-use)

There are 2 forms of authentication to use the Hospitable API. Here's a short rundown on when you'd use either:

* [OAuth Authorization flow for Vendors.](#oauth-authorization-for-vendors)
  + Like when logging into a website with Google or Twitter, Hospitable has it's own OAuth2 Authorization flow. This allows any third-party to integrate directly with Hospitable, without requiring the user to manually share credentials insecurely. This has the added bonus of being extra secure for both Hospitable users, and developers wishing to build on our platform.
* [Personal Access Tokens (PATs) for Personal API use.](#personal-access-tokens)
  + As the name suggests, typically used for Personal API access. These tokens are scoped to your Hospitable account only, and should not be shared with any third-parties. You should only use these tokens for building and testing **your own** Hospitable integration.

If you require any further information on which grant better suits your use case, [get in touch with support](mailto:support@hospitable.com).

## [OAuth Authorization for Vendors](#oauth-authorization-for-vendors)

If you intend on building a Hospitable integration for others, you'll need to use our OAuth2 Authorization code flow. This follows the OAuth2 standard, which you can [learn more about here](https://www.oauth.com/oauth2-servers/access-tokens/authorization-code-request/).

#### [Applying to become an Approved Vendor](#applying-to-become-an-approved-vendor)

To get started, you'll need to request your own Vendor client credentials [via this form](https://form.typeform.com/to/n8bZPJIm). You'll be required to provide a:

* Technical point of contact
* Name and description of your app and the planned integration with Hospitable
* Requested scopes
* Hosted URL for your app's logo (in square format) - .png or .jpg
* A customer-facing description of what your app will do, this displays to the user
* A redirection URL (this should be inside your app, where you will handle the provided OAuth authorize code)
* A webhooks URL (where you'll receive all webhooks)

> ❗ We are **NOT** accepting applications for certain categories of vendors, including AI Chatbots!

You can typically expect a response to your application within a few days. We may reach out for more information.

Once your request is approved, you will be given access to our [Partner Portal](V2/Partner-Portal.md) where you can generate your client credentials, set redirect URLs and add webhook URLs.

---

### [Two ways to initiate the connection with your app](#two-ways-to-initiate-the-connection-with-your-app)

There are 2 ways a user can initiate the connection:

**One-click OAuth initiated in Hospitable by a logged-in user**

Once you have enabled OAuth, we will publish a dedicated page for your product in our [Apps marketplace](https://my.hospitable.com/apps). A logged in user will be able to initiate the connection through a Get Started button on this page.

This redirects them directly to your configured redirect URL with an authorization `code` added as a parameter to the URL. This eliminates the step where they have to be brought to a new page where they click to authorize the connection.

**Standard OAuth flow initiated by your customer from your app**

This is initiated in your app. You must bring the user to the Hospitable Authorization page, where they will be asked to login and then click to authorize the connection.

---

### [1. Setting your redirect URL](#1-setting-your-redirect-url)

When you create your client credentials in the Partner Portal, you will be able to configure the redirect URL, where we will send your customers after they have authorized the connection between your app and their Hospitable account.

By default, this URL is used for both methods described above. If you wish to set a different URL for the one-click connection, let our team know and we can configure that for you.

You also have the option to set a custom URL for the one-click connection. We will not pass the authorization code, which means the user will simply be brought to your site, and you will need to navigate them at some point to the Hospitable Authorization page, following the standard flow. The custom URL supports state so you can associate the request with the user.

### [2. Setting up the OAuth flow](#2-setting-up-the-oauth-flow)

#### [a. Lead the user to authorize the connection](#a-lead-the-user-to-authorize-the-connection)

> This step is skipped if the customer initiates the connection from Hospitable's side using the One-click OAuth. Upon redirect to your page, we will pass the code which you can already use to request for the tokens in step by step.

You will need to create a button or link within your app that redirects your user to the Hospitable Authorization page:

```


https://auth.hospitable.com/oauth/authorize?client_id=<your vendor id>&response_type=code


```

The `response_type=code` tells the authorization server that the application is initiating the authorization code flow which is an [OAuth 2.0 grant type](https://developer.okta.com/blog/2018/04/10/oauth-authorization-code-grant-type). Note: the `code` is a string, and not a placeholder to be replaced with any value.

> 💡 Use the state parameter to associate an authorization request to a customer
>
> You can optionally add the `?state=<string>` parameter to the authorization URL which, in addition to adding a layer of security, allows you to identify the source of the request, e.g. identify the customer that just completed the flow.
> The `state` value will passed back to you by adding it to your the redirect URL, which you can compare with the value you stored earlier.
>
> [Learn more about it here.](https://auth0.com/docs/secure/attack-protection/state-parameters)

The Hospitable Authorization page will initially present them with a login page. (this will always be presented as long as they initiated from your page, even if they were already logged in to Hospitable in the same browser session). After providing their credentials, they will be asked to Authorize the connection with your app.

#### [b. Handle the redirect](#b-handle-the-redirect)

When the user clicks "Authorize" they'll be redirected to the URL that you configured in the Partner Portal. There will be an authorization `code` added as a parameter to the URL.

https://not-hospitable.com/redirect?code=def2020087...

This will also include the `state` if you had provide that earlier.

#### [c. Request for the access token](#c-request-for-the-access-token)

Make a request to our OAuth2 server at `https://auth.hospitable.com/oauth/token`, providing your client credentials, `"authorization_code"` grant type and the provided `code` from the redirection.

The request should look like this:

```


curl --request POST \



--url https://auth.hospitable.com/oauth/token \



--header 'Content-Type: application/json' \



--data '{



"client_id": "<your vendor id>",



"client_secret": "<your vendor secret>",



"grant_type": "authorization_code",



"code": "def5020087..."



}'


```

With a response of:

```


{



"token_type": "Bearer",



"expires_in": 43200,



"access_token": "eyJ0eXA...",



"refresh_token": "def502005..."



}


```

Once you have the `access_token`, you can start making API requests on behalf of the user by including it in the Authorization header of each request:

```


curl --request GET \



--url https://public.api.hospitable.com/properties \



--header 'Authorization: Bearer <token>'


```

> 🚧 **Token validity**
>
> The `access_token` expires after 12 hours. You will need to request for new access tokens using the `refresh_token`.
>
> 📘 **Check your database columns!**
>
> Tokens are quite large! Access tokens ~1,200 chars and Refresh tokens ~1,000 chars respectively. If your database columns aren't configured correctly, you might experience unexpected issues with accessing the API, or refreshing due to truncation.

### [Refreshing your access tokens](#refreshing-your-access-tokens)

When the access token expires, you'll receive a `401 Unauthenticated` error from your API requests. To resolve this, you'll need to refresh your access using the `refresh_token` that was also provided in the authorization response.

The refresh request looks like this:

```


curl --request POST \



--url https://auth.hospitable.com/oauth/token \



--header 'Content-Type: application/json' \



--data '{



"client_id": "<your vendor id>",



"client_secret": "<your vendor secret>",



"grant_type": "refresh_token",



"refresh_token": "<the refresh token>"



}'


```

This will provide a response identical step 3 when you first requested the tokens. The response will provide you with a new set of access\_token and refresh\_token.

> 🚧 Refresh tokens expire!
>
> If your integration doesn't refresh Access Tokens immediately after expiry (which is common in some use cases where you may not need constant API access), you'll need to be careful - **Refresh Tokens expire after 90 days**. We recommend refreshing all tokens on a regular interval to ensure Hosts don't need to keep re-authorising your application.

---

## [Personal Access Tokens for Hospitable users](#personal-access-tokens-for-hospitable-users)

If you're just trying to play around with your Hospitable account programatically, or have an existing system built to automate your workflows, you can use Personal Access Tokens which provides the same access to endpoints as vendors.

> 📘 Choose the right grant!
>
> If you're building a Hospitable integration to be used by others, you will need to use our [OAuth2 Authorization flow](#oauth-authorization-for-vendors). We do not recommend storing other users' Personal Access Tokens.

To get started with Personal Access Tokens, start by logging into your Hospitable account and visiting your [API keys](https://my.hospitable.com/apps/api-keys) section in the apps settings.

Once there, you can create and manage your Personal Access Tokens. Click "+ Add new" in the top right to create a new one, giving it any name you'd like:

![](https://files.readme.io/a2b24de-image.png)

This is the only step required to gain authentication for your account. Now, any requests you make to our API should include the `Authorization` header, with `Bearer <token>` as the value.

```


curl --request GET \



--url https://public.api.hospitable.com/v2/properties \



--header 'Accept: application/json' \



--header 'Authorization: Bearer <token>' \



--header 'Content-Type: '


```

[Authentication](#authentication "Authentication")[What Authentication should I use?](#what-authentication-should-i-use "What Authentication should I use?")[OAuth Authorization for Vendors](#oauth-authorization-for-vendors "OAuth Authorization for Vendors")[Two ways to initiate the connection with your app](#two-ways-to-initiate-the-connection-with-your-app "Two ways to initiate the connection with your app")[1. Setting your redirect URL](#1-setting-your-redirect-url "1. Setting your redirect URL")[2. Setting up the OAuth flow](#2-setting-up-the-oauth-flow "2. Setting up the OAuth flow")[Refreshing your access tokens](#refreshing-your-access-tokens "Refreshing your access tokens")[Personal Access Tokens for Hospitable users](#personal-access-tokens-for-hospitable-users "Personal Access Tokens for Hospitable users")