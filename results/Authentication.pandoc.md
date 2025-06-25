::::::::::::::::::::::::::::::::::::::: {.sl-w-full .sl-mx-auto .sl-px-20 .sl-pt-20 .sl-pb-8 test="project-page" style="max-width: 1500px;"}
:::::::::::::::::::::::::::::::::::::: sl-elements-article
::::::::::::::::::::::::::::::::::::: {.sl-flex .sl-relative}
:::::::::::::::::::::::::::::::: {.sl-prose .sl-markdown-viewer .sl-elements-article-content .sl-overflow-x-auto .sl-overflow-y-auto .sl-flex-1 .sl-p-2}
# Authentication {#authentication .sl-text-5xl .sl-leading-tight .sl-font-prose .sl-font-bold .sl-text-heading}

------------------------------------------------------------------------

Hospitable protects our API endpoints using Personal Access Tokens, and
[OAuth 2.0](https://tools.ietf.org/html/rfc6749){rel="noreferrer"
target="_blank"}\'s Authorization flow grants. Depending on your
application use case, it might depend which authentication grant you
choose to go with.

### [](#what-authentication-should-i-use){.sl-link .sl-link-heading__link .sl-inline-flex .sl-items-center .sl-text-current} {#what-authentication-should-i-use .sl-link-heading .sl-text-2xl .sl-leading-snug .sl-font-prose .sl-font-semibold .sl-text-heading}

<div>

What Authentication should I use?

</div>

::: {.sl-link-heading__icon .sl-text-base .sl-ml-4 .sl-text-muted}
:::

There are 2 forms of authentication to use the Hospitable API. Here\'s a
short rundown on when you\'d use either:

- [OAuth Authorization flow for
  Vendors.](#oauth-authorization-for-vendors)
  - Like when logging into a website with Google or Twitter, Hospitable
    has it\'s own OAuth2 Authorization flow. This allows any third-party
    to integrate directly with Hospitable, without requiring the user to
    manually share credentials insecurely. This has the added bonus of
    being extra secure for both Hospitable users, and developers wishing
    to build on our platform.
- [Personal Access Tokens (PATs) for Personal API
  use.](#personal-access-tokens)
  - As the name suggests, typically used for Personal API access. These
    tokens are scoped to your Hospitable account only, and should not be
    shared with any third-parties. You should only use these tokens for
    building and testing **your own** Hospitable integration.

If you require any further information on which grant better suits your
use case, [get in touch with support](mailto:support@hospitable.com).

## [](#oauth-authorization-for-vendors){.sl-link .sl-link-heading__link .sl-inline-flex .sl-items-center .sl-text-current} {#oauth-authorization-for-vendors .sl-link-heading .sl-text-4xl .sl-leading-tight .sl-font-prose .sl-font-bold .sl-text-heading}

<div>

OAuth Authorization for Vendors

</div>

::: {.sl-link-heading__icon .sl-text-base .sl-ml-4 .sl-text-muted}
:::

If you intend on building a Hospitable integration for others, you\'ll
need to use our OAuth2 Authorization code flow. This follows the OAuth2
standard, which you can [learn more about
here](https://www.oauth.com/oauth2-servers/access-tokens/authorization-code-request/){rel="noreferrer"
target="_blank"}.

#### [](#applying-to-become-an-approved-vendor){.sl-link .sl-link-heading__link .sl-inline-flex .sl-items-center .sl-text-current} {#applying-to-become-an-approved-vendor .sl-link-heading .sl-text-paragraph .sl-leading-snug .sl-font-prose .sl-font-semibold .sl-text-heading}

<div>

Applying to become an Approved Vendor

</div>

::: {.sl-link-heading__icon .sl-text-base .sl-ml-4 .sl-text-muted}
:::

To get started, you\'ll need to request your own Vendor client
credentials [via this
form](https://form.typeform.com/to/n8bZPJIm){rel="noreferrer"
target="_blank"}. You\'ll be required to provide a:

- Technical point of contact
- Name and description of your app and the planned integration with
  Hospitable
- Requested scopes
- Hosted URL for your app\'s logo (in square format) - .png or .jpg
- A customer-facing description of what your app will do, this displays
  to the user
- A redirection URL (this should be inside your app, where you will
  handle the provided OAuth authorize code)
- A webhooks URL (where you\'ll receive all webhooks)

> :::::: {.sl-stack .sl-stack--horizontal .sl-stack--3 .sl-flex .sl-flex-row .sl-items-start .sl-pt-4 .sl-pr-10 .sl-pb-4 .sl-pl-4 .sl-bg-canvas-pure .sl-rounded-xl .sl-border-primary .sl-border-2}
> :::: sl-mt-px
> ::: {testid="icon"}
> :::
> ::::
>
> ::: {.sl-stack .sl-flex .sl-flex-1 .sl-flex-col .sl-items-stretch}
> ❗ We are **NOT** accepting applications for certain categories of
> vendors, including AI Chatbots!
> :::
> ::::::

You can typically expect a response to your application within a few
days. We may reach out for more information.

Once your request is approved, you will be given access to our [Partner
Portal](V2/Partner-Portal.md) where you can generate your client
credentials, set redirect URLs and add webhook URLs.

------------------------------------------------------------------------

### [](#two-ways-to-initiate-the-connection-with-your-app){.sl-link .sl-link-heading__link .sl-inline-flex .sl-items-center .sl-text-current} {#two-ways-to-initiate-the-connection-with-your-app .sl-link-heading .sl-text-2xl .sl-leading-snug .sl-font-prose .sl-font-semibold .sl-text-heading}

<div>

Two ways to initiate the connection with your app

</div>

::: {.sl-link-heading__icon .sl-text-base .sl-ml-4 .sl-text-muted}
:::

There are 2 ways a user can initiate the connection:

**One-click OAuth initiated in Hospitable by a logged-in user**

Once you have enabled OAuth, we will publish a dedicated page for your
product in our [Apps
marketplace](https://my.hospitable.com/apps){rel="noreferrer"
target="_blank"}. A logged in user will be able to initiate the
connection through a Get Started button on this page.

This redirects them directly to your configured redirect URL with an
authorization `code`{.sl-font-mono .sl-font-medium .sl-mx-0.5 .sl-px-1
.sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded .sl-border
style="font-size: 0.8125em;"} added as a parameter to the URL. This
eliminates the step where they have to be brought to a new page where
they click to authorize the connection.

**Standard OAuth flow initiated by your customer from your app**

This is initiated in your app. You must bring the user to the Hospitable
Authorization page, where they will be asked to login and then click to
authorize the connection.

------------------------------------------------------------------------

### [](#1-setting-your-redirect-url){.sl-link .sl-link-heading__link .sl-inline-flex .sl-items-center .sl-text-current} {#1-setting-your-redirect-url .sl-link-heading .sl-text-2xl .sl-leading-snug .sl-font-prose .sl-font-semibold .sl-text-heading}

<div>

1\. Setting your redirect URL

</div>

::: {.sl-link-heading__icon .sl-text-base .sl-ml-4 .sl-text-muted}
:::

When you create your client credentials in the Partner Portal, you will
be able to configure the redirect URL, where we will send your customers
after they have authorized the connection between your app and their
Hospitable account.

By default, this URL is used for both methods described above. If you
wish to set a different URL for the one-click connection, let our team
know and we can configure that for you.

You also have the option to set a custom URL for the one-click
connection. We will not pass the authorization code, which means the
user will simply be brought to your site, and you will need to navigate
them at some point to the Hospitable Authorization page, following the
standard flow. The custom URL supports state so you can associate the
request with the user.

### [](#2-setting-up-the-oauth-flow){.sl-link .sl-link-heading__link .sl-inline-flex .sl-items-center .sl-text-current} {#2-setting-up-the-oauth-flow .sl-link-heading .sl-text-2xl .sl-leading-snug .sl-font-prose .sl-font-semibold .sl-text-heading}

<div>

2\. Setting up the OAuth flow

</div>

::: {.sl-link-heading__icon .sl-text-base .sl-ml-4 .sl-text-muted}
:::

#### [](#a-lead-the-user-to-authorize-the-connection){.sl-link .sl-link-heading__link .sl-inline-flex .sl-items-center .sl-text-current} {#a-lead-the-user-to-authorize-the-connection .sl-link-heading .sl-text-paragraph .sl-leading-snug .sl-font-prose .sl-font-semibold .sl-text-heading}

<div>

a\. Lead the user to authorize the connection

</div>

::: {.sl-link-heading__icon .sl-text-base .sl-ml-4 .sl-text-muted}
:::

> :::::: {.sl-stack .sl-stack--horizontal .sl-stack--3 .sl-flex .sl-flex-row .sl-items-start .sl-pt-4 .sl-pr-10 .sl-pb-4 .sl-pl-4 .sl-bg-canvas-pure .sl-rounded-xl .sl-border-primary .sl-border-2}
> :::: sl-mt-px
> ::: {testid="icon"}
> :::
> ::::
>
> ::: {.sl-stack .sl-flex .sl-flex-1 .sl-flex-col .sl-items-stretch}
> This step is skipped if the customer initiates the connection from
> Hospitable\'s side using the One-click OAuth. Upon redirect to your
> page, we will pass the code which you can already use to request for
> the tokens in step by step.
> :::
> ::::::

You will need to create a button or link within your app that redirects
your user to the Hospitable Authorization page:

``` {.sl-code-viewer .sl-grid .sl-inverted .sl-overflow-x-hidden .sl-overflow-y-hidden .sl-relative .sl-bg-canvas .sl-outline-none .sl-rounded-lg .focus:sl-ring .sl-ring-primary .sl-ring-opacity-50 .sl-group role="group" tabindex="0"}
https://auth.hospitable.com/oauth/authorize?client_id=<your vendor id>&response_type=code
```

The `response_type=code`{.sl-font-mono .sl-font-medium .sl-mx-0.5
.sl-px-1 .sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded .sl-border
style="font-size: 0.8125em;"} tells the authorization server that the
application is initiating the authorization code flow which is an [OAuth
2.0 grant
type](https://developer.okta.com/blog/2018/04/10/oauth-authorization-code-grant-type){rel="noreferrer"
target="_blank"}. Note: the `code`{.sl-font-mono .sl-font-medium
.sl-mx-0.5 .sl-px-1 .sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded
.sl-border style="font-size: 0.8125em;"} is a string, and not a
placeholder to be replaced with any value.

> :::::: {.sl-stack .sl-stack--horizontal .sl-stack--3 .sl-flex .sl-flex-row .sl-items-start .sl-pt-4 .sl-pr-10 .sl-pb-4 .sl-pl-4 .sl-bg-canvas-pure .sl-rounded-xl .sl-border-primary .sl-border-2}
> :::: sl-mt-px
> ::: {testid="icon"}
> :::
> ::::
>
> ::: {.sl-stack .sl-flex .sl-flex-1 .sl-flex-col .sl-items-stretch}
> 💡 Use the state parameter to associate an authorization request to a
> customer
>
> You can optionally add the `?state=<string>`{.sl-font-mono
> .sl-font-medium .sl-mx-0.5 .sl-px-1 .sl-py-0.5 .sl-bg-code
> .sl-text-on-code .sl-rounded .sl-border style="font-size: 0.8125em;"}
> parameter to the authorization URL which, in addition to adding a
> layer of security, allows you to identify the source of the request,
> e.g. identify the customer that just completed the flow. The
> `state`{.sl-font-mono .sl-font-medium .sl-mx-0.5 .sl-px-1 .sl-py-0.5
> .sl-bg-code .sl-text-on-code .sl-rounded .sl-border
> style="font-size: 0.8125em;"} value will passed back to you by adding
> it to your the redirect URL, which you can compare with the value you
> stored earlier.
>
> [Learn more about it
> here.](https://auth0.com/docs/secure/attack-protection/state-parameters){rel="noreferrer"
> target="_blank"}
> :::
> ::::::

The Hospitable Authorization page will initially present them with a
login page. (this will always be presented as long as they initiated
from your page, even if they were already logged in to Hospitable in the
same browser session). After providing their credentials, they will be
asked to Authorize the connection with your app.

#### [](#b-handle-the-redirect){.sl-link .sl-link-heading__link .sl-inline-flex .sl-items-center .sl-text-current} {#b-handle-the-redirect .sl-link-heading .sl-text-paragraph .sl-leading-snug .sl-font-prose .sl-font-semibold .sl-text-heading}

<div>

b\. Handle the redirect

</div>

::: {.sl-link-heading__icon .sl-text-base .sl-ml-4 .sl-text-muted}
:::

When the user clicks \"Authorize\" they\'ll be redirected to the URL
that you configured in the Partner Portal. There will be an
authorization `code`{.sl-font-mono .sl-font-medium .sl-mx-0.5 .sl-px-1
.sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded .sl-border
style="font-size: 0.8125em;"} added as a parameter to the URL.

::::::::: {.sl-code-viewer .sl-grid .sl-inverted .sl-overflow-x-hidden .sl-overflow-y-hidden .sl-relative .sl-bg-canvas .sl-outline-none .sl-rounded-lg .focus:sl-ring .sl-ring-primary .sl-ring-opacity-50 .sl-group role="group" tabindex="0"}
:::::: {.sl-code-viewer__scroller .sl-overflow-x-auto .sl-overflow-y-auto style="max-height: 500px;"}
::::: {.sl-code-highlight .prism-code .language-undefined style="padding: 12px 15px; font-family: var(--font-code); font-size: var(--fs-code); line-height: var(--lh-code);"}
:::: sl-flex
::: {.sl-flex-1 .sl-break-all}
[https://not-hospitable.com/redirect?code=def2020087\...]{.token .plain}
:::
::::
:::::
::::::

:::: {.sl-absolute .sl-right-0 .sl-pr-2 .sl-invisible .group-hover:sl-visible .sl-invisible testid="copy-button" style="top: 9px;"}
::: sl-mx-0
:::
::::
:::::::::

This will also include the `state`{.sl-font-mono .sl-font-medium
.sl-mx-0.5 .sl-px-1 .sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded
.sl-border style="font-size: 0.8125em;"} if you had provide that
earlier.

#### [](#c-request-for-the-access-token){.sl-link .sl-link-heading__link .sl-inline-flex .sl-items-center .sl-text-current} {#c-request-for-the-access-token .sl-link-heading .sl-text-paragraph .sl-leading-snug .sl-font-prose .sl-font-semibold .sl-text-heading}

<div>

c\. Request for the access token

</div>

::: {.sl-link-heading__icon .sl-text-base .sl-ml-4 .sl-text-muted}
:::

Make a request to our OAuth2 server at
`https://auth.hospitable.com/oauth/token`{.sl-font-mono .sl-font-medium
.sl-mx-0.5 .sl-px-1 .sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded
.sl-border style="font-size: 0.8125em;"}, providing your client
credentials, `"authorization_code"`{.sl-font-mono .sl-font-medium
.sl-mx-0.5 .sl-px-1 .sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded
.sl-border style="font-size: 0.8125em;"} grant type and the provided
`code`{.sl-font-mono .sl-font-medium .sl-mx-0.5 .sl-px-1 .sl-py-0.5
.sl-bg-code .sl-text-on-code .sl-rounded .sl-border
style="font-size: 0.8125em;"} from the redirection.

The request should look like this:

``` {.sl-code-viewer .sl-grid .sl-inverted .sl-overflow-x-hidden .sl-overflow-y-hidden .sl-relative .sl-bg-canvas .sl-outline-none .sl-rounded-lg .focus:sl-ring .sl-ring-primary .sl-ring-opacity-50 .sl-group role="group" tabindex="0"}
curl --request POST \  --url https://auth.hospitable.com/oauth/token \  --header 'Content-Type: application/json' \  --data '{  "client_id": "<your vendor id>",   "client_secret": "<your vendor secret>",   "grant_type": "authorization_code",  "code": "def5020087..."}'
```

With a response of:

``` {.sl-code-viewer .sl-grid .sl-inverted .sl-overflow-x-hidden .sl-overflow-y-hidden .sl-relative .sl-bg-canvas .sl-outline-none .sl-rounded-lg .focus:sl-ring .sl-ring-primary .sl-ring-opacity-50 .sl-group role="group" tabindex="0"}
{  "token_type": "Bearer",  "expires_in": 43200,  "access_token": "eyJ0eXA...",  "refresh_token": "def502005..."}
```

Once you have the `access_token`{.sl-font-mono .sl-font-medium
.sl-mx-0.5 .sl-px-1 .sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded
.sl-border style="font-size: 0.8125em;"}, you can start making API
requests on behalf of the user by including it in the Authorization
header of each request:

``` {.sl-code-viewer .sl-grid .sl-inverted .sl-overflow-x-hidden .sl-overflow-y-hidden .sl-relative .sl-bg-canvas .sl-outline-none .sl-rounded-lg .focus:sl-ring .sl-ring-primary .sl-ring-opacity-50 .sl-group role="group" tabindex="0"}
curl --request GET \  --url https://public.api.hospitable.com/properties \    --header 'Authorization: Bearer <token>'
```

> :::::: {.sl-stack .sl-stack--horizontal .sl-stack--3 .sl-flex .sl-flex-row .sl-items-start .sl-pt-4 .sl-pr-10 .sl-pb-4 .sl-pl-4 .sl-bg-canvas-pure .sl-rounded-xl .sl-border-primary .sl-border-2}
> :::: sl-mt-px
> ::: {testid="icon"}
> :::
> ::::
>
> ::: {.sl-stack .sl-flex .sl-flex-1 .sl-flex-col .sl-items-stretch}
> 🚧 **Token validity**
>
> The `access_token`{.sl-font-mono .sl-font-medium .sl-mx-0.5 .sl-px-1
> .sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded .sl-border
> style="font-size: 0.8125em;"} expires after 12 hours. You will need to
> request for new access tokens using the `refresh_token`{.sl-font-mono
> .sl-font-medium .sl-mx-0.5 .sl-px-1 .sl-py-0.5 .sl-bg-code
> .sl-text-on-code .sl-rounded .sl-border style="font-size: 0.8125em;"}.
>
> 📘 **Check your database columns!**
>
> Tokens are quite large! Access tokens \~1,200 chars and Refresh tokens
> \~1,000 chars respectively. If your database columns aren\'t
> configured correctly, you might experience unexpected issues with
> accessing the API, or refreshing due to truncation.
> :::
> ::::::

### [](#refreshing-your-access-tokens){.sl-link .sl-link-heading__link .sl-inline-flex .sl-items-center .sl-text-current} {#refreshing-your-access-tokens .sl-link-heading .sl-text-2xl .sl-leading-snug .sl-font-prose .sl-font-semibold .sl-text-heading}

<div>

Refreshing your access tokens

</div>

::: {.sl-link-heading__icon .sl-text-base .sl-ml-4 .sl-text-muted}
:::

When the access token expires, you\'ll receive a
`401 Unauthenticated`{.sl-font-mono .sl-font-medium .sl-mx-0.5 .sl-px-1
.sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded .sl-border
style="font-size: 0.8125em;"} error from your API requests. To resolve
this, you\'ll need to refresh your access using the
`refresh_token`{.sl-font-mono .sl-font-medium .sl-mx-0.5 .sl-px-1
.sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded .sl-border
style="font-size: 0.8125em;"} that was also provided in the
authorization response.

The refresh request looks like this:

``` {.sl-code-viewer .sl-grid .sl-inverted .sl-overflow-x-hidden .sl-overflow-y-hidden .sl-relative .sl-bg-canvas .sl-outline-none .sl-rounded-lg .focus:sl-ring .sl-ring-primary .sl-ring-opacity-50 .sl-group role="group" tabindex="0"}
curl --request POST \  --url https://auth.hospitable.com/oauth/token \  --header 'Content-Type: application/json' \  --data '{  "client_id": "<your vendor id>",   "client_secret": "<your vendor secret>",   "grant_type": "refresh_token",  "refresh_token": "<the refresh token>"}'
```

This will provide a response identical step 3 when you first requested
the tokens. The response will provide you with a new set of access_token
and refresh_token.

> :::::: {.sl-stack .sl-stack--horizontal .sl-stack--3 .sl-flex .sl-flex-row .sl-items-start .sl-pt-4 .sl-pr-10 .sl-pb-4 .sl-pl-4 .sl-bg-canvas-pure .sl-rounded-xl .sl-border-primary .sl-border-2}
> :::: sl-mt-px
> ::: {testid="icon"}
> :::
> ::::
>
> ::: {.sl-stack .sl-flex .sl-flex-1 .sl-flex-col .sl-items-stretch}
> 🚧 Refresh tokens expire!
>
> If your integration doesn\'t refresh Access Tokens immediately after
> expiry (which is common in some use cases where you may not need
> constant API access), you\'ll need to be careful - **Refresh Tokens
> expire after 90 days**. We recommend refreshing all tokens on a
> regular interval to ensure Hosts don\'t need to keep re-authorising
> your application.
> :::
> ::::::

------------------------------------------------------------------------

## [](#personal-access-tokens-for-hospitable-users){.sl-link .sl-link-heading__link .sl-inline-flex .sl-items-center .sl-text-current} {#personal-access-tokens-for-hospitable-users .sl-link-heading .sl-text-4xl .sl-leading-tight .sl-font-prose .sl-font-bold .sl-text-heading}

<div>

Personal Access Tokens for Hospitable users

</div>

::: {.sl-link-heading__icon .sl-text-base .sl-ml-4 .sl-text-muted}
:::

If you\'re just trying to play around with your Hospitable account
programatically, or have an existing system built to automate your
workflows, you can use Personal Access Tokens which provides the same
access to endpoints as vendors.

> :::::: {.sl-stack .sl-stack--horizontal .sl-stack--3 .sl-flex .sl-flex-row .sl-items-start .sl-pt-4 .sl-pr-10 .sl-pb-4 .sl-pl-4 .sl-bg-canvas-pure .sl-rounded-xl .sl-border-primary .sl-border-2}
> :::: sl-mt-px
> ::: {testid="icon"}
> :::
> ::::
>
> ::: {.sl-stack .sl-flex .sl-flex-1 .sl-flex-col .sl-items-stretch}
> 📘 Choose the right grant!
>
> If you\'re building a Hospitable integration to be used by others, you
> will need to use our [OAuth2 Authorization
> flow](#oauth-authorization-for-vendors). We do not recommend storing
> other users\' Personal Access Tokens.
> :::
> ::::::

To get started with Personal Access Tokens, start by logging into your
Hospitable account and visiting your [API
keys](https://my.hospitable.com/apps/api-keys){rel="noreferrer"
target="_blank"} section in the apps settings.

Once there, you can create and manage your Personal Access Tokens. Click
\"+ Add new\" in the top right to create a new one, giving it any name
you\'d like:

<figure>
<div
class="sl-product-image sl-overflow-x-hidden sl-overflow-y-hidden sl-rounded-xl sl-border-body sl-border-2 hover:sl-shadow sl-cursor-zoom-in sl-transform sl-duration-300 hover:sl-translate-x-2 hover:sl--translate-y-2"
style="--shadow-md: -8px 8px 0 0 var(--color-text);">
<img src="https://files.readme.io/a2b24de-image.png"
class="sl-image sl-overflow-x-hidden sl-overflow-y-hidden sl-mx-auto sl-bg-canvas-pure sl-border-body" />
</div>
</figure>

This is the only step required to gain authentication for your account.
Now, any requests you make to our API should include the
`Authorization`{.sl-font-mono .sl-font-medium .sl-mx-0.5 .sl-px-1
.sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded .sl-border
style="font-size: 0.8125em;"} header, with
`Bearer <token>`{.sl-font-mono .sl-font-medium .sl-mx-0.5 .sl-px-1
.sl-py-0.5 .sl-bg-code .sl-text-on-code .sl-rounded .sl-border
style="font-size: 0.8125em;"} as the value.

``` {.sl-code-viewer .sl-grid .sl-inverted .sl-overflow-x-hidden .sl-overflow-y-hidden .sl-relative .sl-bg-canvas .sl-outline-none .sl-rounded-lg .focus:sl-ring .sl-ring-primary .sl-ring-opacity-50 .sl-group role="group" tabindex="0"}
curl --request GET \  --url https://public.api.hospitable.com/v2/properties \  --header 'Accept: application/json' \  --header 'Authorization: Bearer <token>' \  --header 'Content-Type: '
```
::::::::::::::::::::::::::::::::

:::::: {.sl-markdown-viewer-toc .sl-w-60 .sl-pl-16}
::::: {.sl-sticky .sl-top-0}
:::: {.sl-overflow-y-auto .sl-absolute .sl-w-full .sl-h-screen}
::: sl-py-8
[Authentication](#authentication "Authentication"){.sl-block .sl-text-sm
.sl-font-medium .sl-truncate .sl-py-1 .sl-pr-2 .sl-pl-4 .sl-text-primary
.hover:sl-text-primary-dark .sl-border-primary .sl-border-l-2}[What
Authentication should I
use?](#what-authentication-should-i-use "What Authentication should I use?"){.sl-block
.sl-text-sm .sl-font-medium .sl-truncate .sl-py-1 .sl-pr-2 .sl-pl-6
.sl-text-muted .hover:sl-text-primary-dark .sl-border-light
.sl-border-l-2}[OAuth Authorization for
Vendors](#oauth-authorization-for-vendors "OAuth Authorization for Vendors"){.sl-block
.sl-text-sm .sl-font-medium .sl-truncate .sl-py-1 .sl-pr-2 .sl-pl-4
.sl-text-muted .hover:sl-text-primary-dark .sl-border-light
.sl-border-l-2}[Two ways to initiate the connection with your
app](#two-ways-to-initiate-the-connection-with-your-app "Two ways to initiate the connection with your app"){.sl-block
.sl-text-sm .sl-font-medium .sl-truncate .sl-py-1 .sl-pr-2 .sl-pl-6
.sl-text-muted .hover:sl-text-primary-dark .sl-border-light
.sl-border-l-2}[1. Setting your redirect
URL](#1-setting-your-redirect-url "1. Setting your redirect URL"){.sl-block
.sl-text-sm .sl-font-medium .sl-truncate .sl-py-1 .sl-pr-2 .sl-pl-6
.sl-text-muted .hover:sl-text-primary-dark .sl-border-light
.sl-border-l-2}[2. Setting up the OAuth
flow](#2-setting-up-the-oauth-flow "2. Setting up the OAuth flow"){.sl-block
.sl-text-sm .sl-font-medium .sl-truncate .sl-py-1 .sl-pr-2 .sl-pl-6
.sl-text-muted .hover:sl-text-primary-dark .sl-border-light
.sl-border-l-2}[Refreshing your access
tokens](#refreshing-your-access-tokens "Refreshing your access tokens"){.sl-block
.sl-text-sm .sl-font-medium .sl-truncate .sl-py-1 .sl-pr-2 .sl-pl-6
.sl-text-muted .hover:sl-text-primary-dark .sl-border-light
.sl-border-l-2}[Personal Access Tokens for Hospitable
users](#personal-access-tokens-for-hospitable-users "Personal Access Tokens for Hospitable users"){.sl-block
.sl-text-sm .sl-font-medium .sl-truncate .sl-py-1 .sl-pr-2 .sl-pl-4
.sl-text-muted .hover:sl-text-primary-dark .sl-border-light
.sl-border-l-2}
:::
::::
:::::
::::::
:::::::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::
