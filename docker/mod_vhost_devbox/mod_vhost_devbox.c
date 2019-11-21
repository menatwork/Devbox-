#include "apr.h"
#include "apr_strings.h"
#include "ap_hooks.h"
#include "apr_lib.h"

#include "httpd.h"
#include "http_config.h"
#include "http_core.h"
#include "http_request.h"  /* for ap_hook_translate_name */
#include "http_protocol.h"
#include "http_log.h"

#include <yaml.h>

#define HOSTNAME         "devbox.localhost"
#define SCHEMA_FILE_NAME ".devbox.yml"

static char *vhost_devbox_schema_read_webroot(request_rec *req,
					      const char *file)
{
	char *webroot = NULL;
	FILE *f = fopen(file, "r");

	if (f == NULL) {
		return NULL;
	}

	yaml_parser_t parser;
	yaml_event_t event;
	int done = 0;

	int mapping_depth = 0;
	int in_project = 0;
	int in_webroot = 0;

	yaml_parser_initialize(&parser);
	yaml_parser_set_input_file(&parser, f);

	while (!done) {
		if (!yaml_parser_parse(&parser, &event)) {
			goto free_return;
		}

		switch (event.type) {
		case YAML_MAPPING_START_EVENT:
			mapping_depth++;
			break;

		case YAML_MAPPING_END_EVENT:
			mapping_depth--;
			if (mapping_depth == 0 && in_project) {
				in_project = 0;
			} else if (mapping_depth == 1 && in_webroot) {
				in_webroot = 0;
			}
			break;

		case YAML_SCALAR_EVENT:
			if (in_webroot && mapping_depth == 2) {
				webroot = apr_pstrdup(req->pool, event.data.scalar.value);
				done = 1;
				break;
			}

			if (in_project
			    && !in_webroot
			    && mapping_depth == 2
			    && strcmp(event.data.scalar.value, "webroot") == 0) {
				in_webroot = 1;
				break;
			}

			if (!in_project
			    && mapping_depth == 1
			    && strcmp(event.data.scalar.value, "project") == 0) {
				in_project = 1;
			}

			break;
			
		case YAML_STREAM_END_EVENT:
			done = 1;
			break;
		}

		yaml_event_delete(&event);
	}
		
free_return:
	yaml_parser_delete(&parser);
	fclose(f);

	return webroot;
}

static char *vhost_devbox_lookup_doc_root(request_rec *req,
					const char *project_dir)
{
	const char *doc_root = ap_document_root(req);

	char *full_project_path;
	apr_filepath_merge(&full_project_path, doc_root, project_dir, 0,
			   req->pool);

	char *schema_file_path;
	apr_filepath_merge(&schema_file_path, full_project_path,
			   SCHEMA_FILE_NAME, 0, req->pool);

	char *webroot = vhost_devbox_schema_read_webroot(req, schema_file_path);
	if (webroot == NULL) {
		return NULL;
	}

	char *new_doc_root;
	apr_filepath_merge(&new_doc_root, full_project_path, webroot, 0,
			   req->pool);

	size_t len = strlen(new_doc_root);
	if (new_doc_root[len - 1] == '/') {
		new_doc_root[len - 1] = '\0';
	}

	return new_doc_root;
}

static char *vhost_match_subdomain(request_rec *req) {
	char *suffix = ap_strchr(req->hostname, '.');
	if (suffix == NULL || strcmp(suffix + 1, HOSTNAME) != 0) {
		return NULL;
	}

	size_t len = (size_t) (suffix - req->hostname);
	char *subdomain = apr_pstrndup(req->pool, req->hostname, len);

	return subdomain;
}

static int vhost_devbox_translate_name(request_rec *req) {
	if (req->uri[0] != '/') {
		/* TODO: when is this path ever hit? */
		return DECLINED;
	}

	char *project_dir = vhost_match_subdomain(req);
	if (project_dir == NULL) {
		/* request to some file that isn't in a subdirectory */
		return DECLINED;
	}

	char *new_doc_root = vhost_devbox_lookup_doc_root(req, project_dir);
	if (new_doc_root == NULL) {
		/* project dir without a schema file */
		return DECLINED;
	}

	req->filename = apr_pstrcat(req->pool, new_doc_root, req->uri, NULL);
	ap_set_context_info(req, NULL, new_doc_root);
	ap_set_document_root(req, new_doc_root);

	return OK;
}

static void register_hooks(apr_pool_t *pool) {
	static const char * const predecessors[] = {"mod_alias.c", NULL};

	ap_hook_translate_name(
		vhost_devbox_translate_name,
		predecessors,
		NULL,
		APR_HOOK_MIDDLE
	);
}

AP_DECLARE_MODULE(vhost_devbox) =
{
	STANDARD20_MODULE_STUFF,
	NULL,  /* Per-directory configuration handler */
	NULL,  /* Merge handler for per-directory configurations */
	NULL,  /* Per-server configuration handler */
	NULL,  /* Merge handler for per-server configurations */
	NULL,  /* Any directives we may have for httpd */
	register_hooks  /* Our hook registering function */
};
